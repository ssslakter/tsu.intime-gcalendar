## Send your TSU schedule to google calendar
This is a simple cli tool to get a schedule from https://intime.tsu.ru/schedule and upload it to your google calendar. (at some point this should be implemented in mobile app, if so this repository is basically useless)
### Quickstart
Clone the repository and install all the dependencies
```sh
git clone https://github.com/Ssslakter/tsu.intime-gcalendar
cd tsu.intime-gcalendar
pip install -r requirements.txt
python ./main.py --help
```
At the first time when started it will ask you to join via Google account to get access to the calendar. 
### Config
To use this app you have to put `config.json` file in the root directory that would contain information about your group and faculty to use them in api.
```json
{
  // get this in the google calendar app settings
  "calendar_id": "<your-calendar-id>@group.calendar.google.com",
  // all fields below must have EXACT names as they are in original tsu.intime app
  "faculty_name": "Научно-образовательный центр \"Высшая ИТ школа\"", 
  "group_name": "972103",
  // used if schedule contains lessons with different groups mentioned
  "allowed_group_names": [
    "972103",
    "972103 (1)",
    null
  ],
  // these lessons will be ignored
  "blacklist": [
    "Элективные дисциплины по физической культуре и спорту"
  ],
  "time_zone": "Asia/Tomsk",
  // it is also possible to add custom lessons that are not in your original schedule
  "custom": [
    {
      "title": "Физкультура",
      "weekday": 2,
      "start": "10:30:00",
      "end": "12:00:00",
      "audience": "Буревестник",
      "lesson_type": "other"
    }
  ]
}
```

