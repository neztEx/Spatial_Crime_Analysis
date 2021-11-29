import React from 'react'
import { Grid, Typography } from "@material-ui/core"
import DatePicker from "./DatePicker"

function getLastWeek() {
  var today = new Date()
  var lastWeek = new Date(
    today.getFullYear(),
    today.getMonth(),
    today.getDate() - 7
  )
  return lastWeek
}

export const DateFilterComp = ({
  selectedStartDate,
  selectedEndDate,
  setSelectedStartDate,
  setSelectedEndDate
}) => {
  const msDay = 60 * 60 * 24 * 1000
  const a = new Date(selectedStartDate)
  const b = new Date(selectedEndDate)
  const dateLength = Math.floor((b - a) / msDay)

  return (
    <>
      <div
        style={{
          display: "flex",
          marginTop: 20,
          justifyContent: "space-between",
          alignItems: "center"
        }}
      >
        <Typography>
          {" "}
          <span style={{ fontWeight: "bold" }}>{dateLength + 1}</span> days
          selected
        </Typography>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center"
          }}
        >
          {/* <div
            style={{
              fontSize: 16,
              marginLeft: 10,
              marginRight: 10,
              cursor: "pointer",
              color: "#0EA7BC"
            }}
            onClick={() =>
              setSelectedStartDate(
                new Date().setMonth(new Date().getMonth() - 12)
              )
            }
          >
            1y
          </div>
          |
          <div
            style={{
              fontSize: 16,
              marginLeft: 10,
              marginRight: 10,
              cursor: "pointer",
              color: "#0EA7BC"
            }}
            onClick={() =>
              setSelectedStartDate(
                new Date().setMonth(new Date().getMonth() - 1)
              )
            }
          >
            1m
          </div>
          |
          <div
            style={{
              fontSize: 16,
              marginLeft: 10,
              cursor: "pointer",
              color: "#0EA7BC"
            }}
            onClick={() => setSelectedStartDate(getLastWeek())}
          >
            1w
          </div> */}
        </div>
      </div>
      <Grid container spacing={2}>
        <Grid item xs={6}>
          <DatePicker
            selectedDate={selectedStartDate}
            setSelectedDate={setSelectedStartDate}
            label={"Start Date"}
          />
        </Grid>
        <Grid item xs={6}>
          <DatePicker
            selectedDate={selectedEndDate}
            setSelectedDate={setSelectedEndDate}
            label={"End Date"}
          />
        </Grid>
      </Grid>
    </>
  )
}
