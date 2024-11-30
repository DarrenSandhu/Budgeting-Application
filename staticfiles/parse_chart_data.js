function parse_chart_data(data) {
    var data_cleaned = data.replace(/&quot;/g, '"').replace(/&amp;/g, '&');
    try {
        var data = JSON.parse(data_cleaned);
    } catch (error) {
        console.error(error);
    }

    return data;
};