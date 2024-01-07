# vcalcopy
Use [vDirSyncer (dockerized)](https://github.com/Bleala/Vdirsyncer-DOCKERIZED) to copy events between calendars. 
Filter and modify events, ping to [healthchecks.io](https://healthchecks.io/docs/http_api/)

## Features

- Copy events from (one or more) _Source_ calendar (ical-Feed, i.e. Google calendar) to _Destination_ Calendar (vCal, i.e. mailbox.org)

- Filter events, i.e. copy only events starting from last week (this also respects ongoing recurring events)

- Modify events depending on _Source_ calendar, i.e. extend start/end time (so your availibility in _Destination_ calendar will also reflect wour way to/from work)

- Removes Organizator and Attendees from events (so mailbox.org will not send bogus declinement mails)

- After every sync job finished, its result and log can be sent to a healthchecks.io instance for monitoring

## Installation

1. Use provided `docker-compose.yml`, but comment out `entrypoint:` and `AUTOSYNC=` lines

1. Execute Bash in the running container, and copy all files from `/vdirsyncer` in this repo, to `/vdirsyncer` in the container.

1. **Important** - please read carefully:

    - If you <u>want to use healthchecks ping</u>, you can edit `cronfile` and adjust the sync time/frequency. Be aware that ENV var `CRON_TIME` **must be SET as commented out** (leading # sign) in `docker-compose.yml / environment` to avoid running two sync processes in parallel

    - If you <u>**don't use** use healthchecks ping</u>, you **must** delete `cronfile` and `notify.sh`, but also set ENV var `CRON_TIME` in your `docker-conmpose.yml / environment` to a correct cron-pattern - at least remove the `#` sign like this: `CRON_TIME=*/8 * * * *`

    (This will be a lot easier when [this pull request](https://github.com/Bleala/Vdirsyncer-DOCKERIZED/pull/14) is merged, and we can remove some workaround)

1. Edit `config` file and set your individual paths, URLs, Credentials. \
You can even add more _Source_ calendars if you want to.

1. Create all paths you have set in filesystem-storage definitions

1. Make all bash scripts executable: `chmod +x *.sh`

1. Initialize Sync via `vdirsyncer discover`

1. Start first sync manually via `vdirsyncer metasync && vdirsyncer sync`. This will fetch all Events from _Source_ calender, store them in the container's filesystem, process all (new/modified) Events via `posthook`-Script and stores resulting (filtered/modified) Events in `upstream` dir. At this moment, we have not yet tried to upload them to the _Destination_ calendar! \
If errors occured, the IDs are listed in `/vdirsyncer/posthook.err` file.

1. Start a second manual sync via `vdirsyncer sync`. Now, all events from `upstream` dir should be uploaded to _Destination_ calendar.

1. If everything went fine, you can exit the container shell, and enable `AUTOSYNC` and `entrypoint` lines in your `docker-compose.yml`, and restart it.


