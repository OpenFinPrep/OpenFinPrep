function keyToColumnLabel(key){
    return key.replace(/_([a-z])/g, (_, letter) => ` ${letter.toUpperCase()}`)
                    .replace(/^\w/, c => c.toUpperCase());
};

export { keyToColumnLabel };