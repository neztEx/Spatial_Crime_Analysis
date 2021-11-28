
//Syntax for use QueryServer.then(fetched_json => <your code>)
const QueryServer = async() => {
    let fetched_json = fetch('http://127.0.0.1:5002/map')
    .then(res => res.json());
    return await fetched_json;
}

export default QueryServer;