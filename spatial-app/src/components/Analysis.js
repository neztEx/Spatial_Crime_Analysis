import React from 'react'
import { BarChartComp, LineChartComp } from "./Charts"
import { Typography } from "@material-ui/core"
import { countBy, map, sortBy } from "lodash"
import capitalise from "lodash.capitalize"
import { raceDict } from "./Arr"

export const Analysis = ({ data, area, race, gender, crimeType }) => {
    const determineRace = (race) => {
        return raceDict[race]
    }

    const groupBy = (data, key) => {
        const result = countBy(data, key)

        const shorten = (val) => {
            if (typeof val === "string" && val.length > 10) {
                return val.substring(0, 10)
            } else {
                return val
            }
        }

        const res = Object.entries(result).map(([value, count]) => ({
            value,
            count
        }))

        return res.map((item) => ({
            ...item,
            value: capitalise(shorten(item.value))
        }))
    }
    const areaData = map(groupBy(data, "area_name"))
    const dateData = map(groupBy(data, "date_occ"))
    const hourData = sortBy(map(groupBy(data, "time_occ")), ["value"])
    const raceData = map(groupBy(data, "vict_descent"))
    const genderData = map(groupBy(data, "vict_sex"))
    const ageData = map(groupBy(data, "vict_age"))
    const crimeTypeData = map(groupBy(data, "crm_cd_desc"))
    const premiseTypeData = map(groupBy(data, "premis_desc"))

    const modifiedRaceData = raceData.map((item) => ({
        ...item,
        value: determineRace(item.value)
    }))

    const avgDailyCrimeCount =
        dateData.reduce((acc, item) => acc + Number(item.count), 0) /
        dateData.length

    // const avgVictimAge =
    //   ageData.reduce((acc, item) => acc + Number(item.count), 0) / ageData.length

    // const avgHourlyCrimeCount =
    //   hourData.reduce((acc, item) => acc + Number(item.count), 0) /
    //   hourData.length

    return (
        <>
            <div
                style={{
                    width: "100%",
                    height: "100%",
                    //   overflow: "hidden"
                    overflow: "visible"
                }}
            >
                <div
                    style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignContent: "center",
                        marginTop: 20,
                        marginBottom: 10
                    }}
                >
                    <Typography>Daily Crime Incidents</Typography>
                    <Typography>
                        Avg Daily Crime Count:{" "}
                        <span style={{ fontWeight: "bold" }}>
                            {avgDailyCrimeCount.toFixed(2)}
                        </span>
                    </Typography>
                </div>
                <LineChartComp data={dateData} height={400} yAxisWidth={20} />

                <div
                    style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignContent: "center",
                        marginTop: 20,
                        marginBottom: 10
                    }}
                >
                    <Typography>Crime Incidents by Time of Day</Typography>
                    {/* <Typography>
            Avg Hourly Count:{" "}
            <span style={{ fontWeight: "bold" }}>
              {avgHourlyCrimeCount.toFixed(2)}
            </span>
          </Typography> */}
                </div>
                <LineChartComp data={hourData} height={400} yAxisWidth={20} />

                {area === "All Areas" && (
                    <>
                        <Typography style={{ marginTop: 20, marginBottom: 10 }}>
                            Crime Incidents by Area
                        </Typography>
                        <BarChartComp
                            data={areaData}
                            height={areaData.length > 3 ? areaData.length * 25 : 90}
                            yAxisWidth={180}
                        />
                    </>
                )}
                {race === "All" && (
                    <>
                        <Typography style={{ marginTop: 20, marginBottom: 10 }}>
                            Crime Incidents by Victim Race
                        </Typography>
                        <BarChartComp
                            data={modifiedRaceData}
                            height={
                                modifiedRaceData.length > 3 ? modifiedRaceData.length * 25 : 90
                            }
                            yAxisWidth={90}
                        />
                    </>
                )}
                {gender === "All" && (
                    <>
                        <Typography style={{ marginTop: 20, marginBottom: 10 }}>
                            Crime Incidents by Victim Gender
                        </Typography>
                        <BarChartComp
                            data={genderData}
                            height={genderData.length > 3 ? genderData.length * 25 : 90}
                            yAxisWidth={90}
                        />
                    </>
                )}
                <div style={{ marginTop: 20, marginBottom: 10 }}>
                    <Typography>Crime Incidents by Victim Age</Typography>
                    {/* <Typography>
          Avg Victim Age:{" "}
          <span style={{ fontWeight: "bold" }}>{avgVictimAge.toFixed(2)}</span>
        </Typography> */}
                </div>
                <BarChartComp
                    data={ageData}
                    height={ageData.length > 3 ? ageData.length * 20 : 90}
                    yAxisWidth={90}
                />
                {crimeType === "ALL CRIME TYPES" && (
                    <>
                        <Typography style={{ marginTop: 20, marginBottom: 10 }}>
                            Crime Incidents by Crime Type
                        </Typography>
                        <BarChartComp
                            data={crimeTypeData}
                            height={crimeTypeData.length > 3 ? crimeTypeData.length * 20 : 90}
                            yAxisWidth={90}
                        />
                    </>
                )}
                <>
                    <Typography style={{ marginTop: 20, marginBottom: 10 }}>
                        Crime Incidents by Premise Type
                    </Typography>
                    <BarChartComp
                        data={premiseTypeData}
                        height={
                            premiseTypeData.length > 3 ? premiseTypeData.length * 20 : 90
                        }
                        yAxisWidth={90}
                    />
                </>
            </div>
        </>
    )
}
