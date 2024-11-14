function keyToColumnLabel(key){
    return key.replace(/_([a-z])/g, (_, letter) => ` ${letter.toUpperCase()}`)
                    .replace(/^\w/, c => c.toUpperCase());
};

function toSearchQuery(params){
    let parts = [];
    for (let k in params){
      if (params[k] !== undefined && params[k] !== '') parts.push(k + "=" + params[k]);
    }
    if (parts.length > 0) return "?" + parts.join("&");
    else return "";
}

function buildUrlWithQuery(url, params){
    return (url.indexOf("?") !== -1 ? url.slice(0, url.indexOf("?")) : url) + toSearchQuery(params);
}

function downloadFile(filename, data) {
    const link = document.createElement('a');
    link.download = filename;
    const url = URL.createObjectURL(data);
    link.href = url;
    link.click();
    URL.revokeObjectURL(url);
}

export { keyToColumnLabel, toSearchQuery, buildUrlWithQuery, downloadFile };