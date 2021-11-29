import React, { useCallback } from "react"
import { Select, MenuItem } from "@material-ui/core"

export default function SelectComp({ title, arr, foo, setFoo }) {
  // const classes = useStyles()

  const handleChange = useCallback(
    (event) => {
      setFoo(event.target.value)
    },
    [foo]
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
              {item}
            </div>
          </MenuItem>
        ))}
      </Select>
    </div>
  )
}
