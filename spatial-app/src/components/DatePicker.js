import React from 'react'
import {format} from "date-fns"
import DateFnsUtils from "@date-io/date-fns"
import {
  MuiPickersUtilsProvider,
  KeyboardDatePicker
} from "@material-ui/pickers"
import debounce from "lodash.debounce"

export default function DatePicker({ selectedDate, setSelectedDate, label }) {
  const handleDateChange = debounce((item) => {
    console.log("i fired...",item)
    setSelectedDate(item)
  }, 2000)

  return (
    <MuiPickersUtilsProvider utils={DateFnsUtils}>
      <KeyboardDatePicker
        disableToolbar
        variant="inline"
        format="MM/dd/yyyy"
        margin="normal"
        id="date-picker-inline"
        label={label}
        value={selectedDate}
        onChange={handleDateChange}
        KeyboardButtonProps={{
          "aria-label": "change date"
        }}
      />
    </MuiPickersUtilsProvider>
  )
}