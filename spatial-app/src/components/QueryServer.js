
//Syntax for use QueryServer.then(fetched_json => <your code>)
export const QueryServer = async() => {
    let fetched_json = fetch('http://127.0.0.1:5002/map')
    .then(res => res.json());
    return await fetched_json;
}

export const location = async function(city) {
    const url = `http://0.0.0.0:5432/location_based_query/${city}`
    console.log(url)
    let fetched_json = fetch(url)
    .then(res => res.json())
    .catch(res => {});
    return await fetched_json;
}