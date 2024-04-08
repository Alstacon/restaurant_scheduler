### Restaurant schedule 
_____
The program accepts JSON-formatted opening hours of a restaurant as an input
and returns the rendered human-readable format as a text output.

#### RUN
- `source venv/bin/activate`
- `python scheduler.py`


Input example:

```azure
{
    "friday": [
        {"type": "open", "value": 46800}
    ],
    "saturday": [
        {"type": "close", "value": 7200},
        {"type": "open", "value": 43200},
        {"type": "close", "value": 50400},
        {"type": "open", "value": 61200},
        {"type": "close", "value": 79200}
    ]
}
```

#### Note
> It is assumed that the schedule is built only for the days transferred to the input.
Missed days are ignored.
