import React, { useCallback } from "react"
import { Select, MenuItem } from "@material-ui/core"
import { raceDict } from "../components/Arr"

export default function SelectRaceComp({ title, arr, foo, setFoo }) {
  const determineRace = (race) => {
    return raceDict[race]
  }

  const handleChange = useCallback(
    (event) => {
      setFoo(event.target.value)
    },
    [setFoo]
  )

  return (
    <div>
      <div style={{ fontSize: 10, marginBottom: 5 }}>{title}</div>
      <Select
        value={foo}
        onChange={handleChange}
        variant="outlined"
        // disableUnderline
        fullWidth
        style={{ display: "flex", width: "100%" }}
      >
        {arr?.map((item, index) => (
          <MenuItem
            key={index}
            value={item}
            style={{
              display: "flex",
              width: "100%",
              alignItems: "center"
            }}
          >
            <div
              style={{
                whiteSpace: "pre-wrap"
              }}
            >
              {determineRace(item)}
            </div>
          </MenuItem>
        ))}
      </Select>
    </div>
  )
}
