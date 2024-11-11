

function Alert({setError, children}){
    return (<div className="alert alert-warning alert-dismissible fade show" role="alert">
        {children}
        <button type="button" onClick={() => setError("")} className="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>);
}

export default Alert;