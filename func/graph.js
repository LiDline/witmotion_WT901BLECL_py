function(msg) {
    if (!msg) { return {}; }  // no data, just return
    const data = JSON.parse(msg.data);  // read the data

    var name = ['X', 'Y', 'Z']
    var colors = ['rgb(255, 0, 0)', 'rgb(0, 128, 0)', 'rgb(0, 0, 255)']

    var trace1 = []
    var trace2 = []
    var trace3 = []

    // Отрисовка графиков
    for( var i = 0 ; i < 3 ; i++ ) {
        trace1.push({
                x: data[0], y: data[i+1], type: "scatter", line: {color: colors[i], width: 2}, "showlegend": false,
                name: name[i], xaxis: 'x1', yaxis: 'y1',
            });
        trace2.push({
                x: data[0], y: data[i+4], type: "scatter", line: {color: colors[i], width: 2}, "showlegend": false,
                name: name[i], xaxis: 'x2', yaxis: 'y2',
            });
        trace2.push({
                x: data[0], y: data[i+7], type: "scatter", line: {color: colors[i], width: 2}, "showlegend": false,
                name: name[i], xaxis: 'x3', yaxis: 'y3',
            });     
    };

    var trace = trace3.concat(trace1.concat(trace2))

    return {
        "data": trace, "layout": {autosize: false,
            height: 700, 
            margin: {
                l: 50,
                r: 50,
                b: 100,
                t: 20,
                pad: 4
              },
            "xaxis": {"title": {"text": "t, сек"}, fixedrange: true, showticklabels: true}, 
            "xaxis2": {"title": {"text": "t, сек"}, fixedrange: true}, 
            "xaxis3": {"title": {"text": "t, сек"}, fixedrange: true}, 
            "yaxis": {"title": {"text": "a, м/с2"}, fixedrange: true}, 
            "yaxis2": {"title": {"text": "w, °/с"}, fixedrange: true}, 
            "yaxis3": {"title": {"text": "A, °"}, fixedrange: true},
            grid: {rows: 3, columns: 1, pattern: 'independent'},
        }
    }
};  // plot the data
