import datetime
import shutil
from pytz import timezone
import icalendar

def termin_anpassen(ics_dateipfad, ziel_ordner, vor_minuten=0, nach_minuten=None):
    # Grenze: alle Events vor der Grenze werden verworfen
    grenze = datetime.date.today() - datetime.timedelta(days=7)

    # Lese die iCalendar-Datei
    with open(ics_dateipfad, 'rb') as f:
        cal_data = f.read()
    cal = icalendar.Calendar.from_ical(cal_data)

    speichern = False

    # Überprüfe jeden Termin in der iCalendar-Datei
    for event in cal.walk('VEVENT'):
        startzeit = event.get('dtstart').dt
        endzeit = event.get('dtend')

        # mailbox.org sendet unsinnige Absage-Mails, falls der Nutzer nicht in der TN-Liste steht
        # lösche daher Organisator und Teilnehmer, da im gespiegelten Event nicht mehr gebraucht
        if 'ORGANIZER' in event:
          del event['ORGANIZER']
        if 'ATTENDEE' in event:
          del event['ATTENDEE']

        rrule = event.get('rrule')
        if rrule is None:
            kein_serientermin = True
        elif 'UNTIL' in rrule:
            ut = rrule['UNTIL'][0]
            if isinstance(ut, datetime.datetime):
                ut = ut.date()
            kein_serientermin = (ut < grenze)
        else:
            kein_serientermin = False

        if endzeit is None:
            endzeit = startzeit + datetime.timedelta(minutes=60)
        else:
            endzeit = endzeit.dt

        if not isinstance(endzeit, datetime.datetime):
            # ganztägiges Event: keine Änderung der Start-/Endzeit
            if kein_serientermin and (endzeit < grenze):
                print(f"Termin '{event.get('summary')} (bis {endzeit})' liegt mehr als eine Woche in der Vergangenheit -- SKIP")
                continue
            speichern = True
        else:
            # Ändere Zeiten um vor_minuten früher und nach_minuten länger
            if (startzeit is not None) and ((vor_minuten != 0) or ((nach_minuten is not None) and (nach_minuten != 0))):
                startzeit -= datetime.timedelta(minutes=vor_minuten)
                if nach_minuten is None:
                    endzeit += datetime.timedelta(minutes=vor_minuten)
                else:
                    endzeit += datetime.timedelta(minutes=nach_minuten)

                # Speichere geänderte Zeiten im Event, im passenden Format
                # mailbox.org fordert eine TZID, wenn vorher eine existierte (bspw weil mehr als 1 TZ im ical sind)
                tiz = event.get('dtstart').params.get('TZID')
                if tiz is not None:
                    startzeit = startzeit.astimezone(timezone(tiz))
                    endzeit = endzeit.astimezone(timezone(tiz))

                # wenn direkt `startzeit` zugewiesen wird, fehlt ggf. die TZ und das Format ist falsch
                event['dtstart'] = icalendar.prop.vDatetime(startzeit)
                event['dtend'] = icalendar.prop.vDatetime(endzeit)

                # Passe auch RECURRENCE-ID und EXDATEs an geänderte Startzeit an
                if vor_minuten != 0:
                    rid = event.get('recurrence-id')
                    if rid is not None:
                        tiz = rid.params.get('TZID')
                        rid = rid.dt - datetime.timedelta(minutes=vor_minuten)
                        if tiz is not None:
                            rid = rid.astimezone(timezone(tiz))
                        event['recurrence-id'] = icalendar.prop.vDatetime(rid)

                    exdates = event.get('exdate')
                    if exdates is not None:
                        adjusted_exdates = []
                        for exdates in ((exdates,) if not isinstance(exdates, list) else exdates):
                            for exdate in exdates.dts:
                                tiz = exdate.params.get('TZID')
                                exdate = exdate.dt - datetime.timedelta(minutes=vor_minuten)
                                if tiz is not None:
                                    exdate = exdate.astimezone(timezone(tiz))
                                adjusted_exdates.append(icalendar.prop.vDDDLists(exdate))
                        event['exdate'] = adjusted_exdates

            if kein_serientermin and (endzeit.date() < grenze):
                print(f"Termin '{event.get('summary')} (bis {endzeit})' liegt mehr als eine Woche in der Vergangenheit -- SKIP")
                continue
            speichern = True

    if speichern:
        # Kopiere die iCalendar-Datei in den Zielordner
        ziel_dateipfad = f"{ziel_ordner}/{ics_dateipfad.split('/')[-1]}"
        with open(ziel_dateipfad, 'wb') as ziel:
            ziel.write(cal.to_ical())
            print(f"Termin '{event.get('summary')} ({startzeit} - {endzeit})' wurde kopiert nach {ziel_dateipfad}.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Terminanpassung und Kopieren von iCalendar-Dateien')
    parser.add_argument('ics_dateipfad', type=str, help='Pfad zur iCalendar-Datei')
    parser.add_argument('ziel_ordner', type=str, help='Pfad zum Zielordner für die kopierte Datei')
    parser.add_argument('--vor_minuten', type=int, default=0, help='Anzahl der Minuten, um die die Startzeit vorverlegt werden soll')
    parser.add_argument('--nach_minuten', type=int, help='Anzahl der Minuten, um die die Endzeit nach hinten verschoben werden soll (default: --vor_minuten)')

    args = parser.parse_args()

    termin_anpassen(args.ics_dateipfad, args.ziel_ordner, args.vor_minuten, args.nach_minuten)