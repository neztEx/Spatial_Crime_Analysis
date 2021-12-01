import {format} from "date-fns"

//Syntax for use QueryServer.then(fetched_json => <your code>)
export const QueryServer = async() => {
    let fetched_json = fetch('http://127.0.0.1:5002/map')
    .then(res => res.json());
    return await fetched_json;
}

export const location = async function(city) {
    const url = `http://0.0.0.0:5432/location_based_query?location=${city}`
    console.log(url)
    let fetched_json = fetch(url)
    .then(res => res.json())
    .catch(res => {});
    return await fetched_json;
}

export const generic = async function(area, start_date, end_date, type_of_crime, gender, race ) {
    const start_timeStamp = format(start_date, 't')
    const end_timeStamp = format(end_date, 't')
    const url = `http://0.0.0.0:5432/aggregate_query?area_name=${area=='All Areas'?'all':area}&start_date=${start_timeStamp}&end_date=${end_timeStamp}&type_of_crime=${type_of_crime=='ALL CRIME TYPES'?'all':type_of_crime}&gender=${gender=='All'?'all':gender}&race=${race=='All'?'all':race}`
    console.log(url)
    let fetched_json = fetch(url)
    .then(res => res.json())
    .catch(res => {});
    return await fetched_json;
}

export const twitter = async function() {
    const url = `http://0.0.0.0:5432/twitter_query`
    console.log(url)
    let fetched_json = fetch(url)
    .then(res => res.json())
    .catch(res => {});
    return await fetched_json;
}