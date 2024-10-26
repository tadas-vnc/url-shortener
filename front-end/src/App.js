import logo from './logo.svg';
import './App.css';
import "../node_modules/bootstrap/dist/css/bootstrap.css";
import { Form, Button, Container, Row, Col, Alert, Card, Navbar, ListGroup, Dropdown , NavItem, NavLink, Nav, InputGroup, ButtonGroup, FormLabel   } from 'react-bootstrap';
import { useState } from 'react';
function App() {
  const [createMode, setCreateMode] = useState(false)
  const [editMode, setEditMode] = useState(false)
  const [deleteMode, setDeleteMode] = useState(false)
  const [newLink, setNewLink] = useState('')
  const [fieldSize, setFieldSize] = useState("380px")
  const [newAlias, setNewAlias] = useState("")
  const [newPassword, setNewPassword] = useState("")
  const [isButtonDisabled, setIsButtonDisabled] = useState(false)
  const [openPopup, setOpenPopup] = useState(false);
  const [resultUrl, setResultUrl] = useState("")
  const [resultPassword, setResultPassword] = useState("")
  
  function back(){
    setCreateMode(false)
    setDeleteMode(false)
    setEditMode(false)
    setResponseMessage("")
  }

  function submit(){
    setIsButtonDisabled(true)
    let data = {}
    if(!newLink){
      setIsButtonDisabled(false)
      setResponseMessage("Source URL is required.")
      setIsSuccess(false)
      return
    }
    data.source_url = newLink
    if(newAlias){
      data.alias = newAlias
    }
    if(newPassword){
      data.password = newPassword
    }
    
    fetch(apiEndpoint + "shorten", {
      body: JSON.stringify(data),
      method: "POST",
      headers: {'content-type':'application/json'}
    }).then(res=>{return res.json();}).then(data=>{
      if(data.error){
        setResponseMessage(data.error)
        setIsSuccess(false)
        setIsButtonDisabled(false)
      }else{
        setResponseMessage(data.success)
        setIsSuccess(true)
        setIsButtonDisabled(false)
        if(data.short_url && data.password){
          setResultUrl(data.short_url)
          setResultPassword(data.password)
          setPopupActive(true)
        }
      }
    }).catch(e=>{
      setResponseMessage("Error during fetch request: "+ e.toString())
      setIsSuccess(false)
    })
  }
  function writeClipboard(id){
    var copyText = document.getElementById(id);
    try{
    copyText.select();
    copyText.setSelectionRange(0, 99999); 
    navigator.clipboard.writeText(copyText.value);}catch{
      copyText.select();
      copyText.setSelectionRange(0, copyText.value.length);
      document.execCommand("copy");
    }
  }
  const [apiEndpoint, setApiEndpoint] = useState(window.location.protocol+"//"+"127.0.0.1:5000/")
  const [isSuccess, setIsSuccess] = useState(true);
  const [responseMessage, setResponseMessage] = useState("")
  const [popupActive, setPopupActive] = useState(false)
  return (
    <div data-bs-theme='dark' className="App">
      {popupActive && 
      <div id='popup'>
        <div>
          <div className='center'>
            <h2 className='text-center w-100'>Url shorten successfully!</h2>
            <div className=''>
            <FormLabel>Short URL</FormLabel>
            <InputGroup style={{width:fieldSize}} className="">
              <Form.Control id="shortenUrl" readOnly={true} aria-label="link" placeholder='https://...' type="text" value={resultUrl}/>
              <InputGroup.Text onClick={(e)=>{writeClipboard("shortenUrl");}}><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M360-240q-33 0-56.5-23.5T280-320v-480q0-33 23.5-56.5T360-880h360q33 0 56.5 23.5T800-800v480q0 33-23.5 56.5T720-240H360Zm0-80h360v-480H360v480ZM200-80q-33 0-56.5-23.5T120-160v-560h80v560h440v80H200Zm160-240v-480 480Z"/></svg>
              </InputGroup.Text>
            </InputGroup>
            </div>
            <div className='w-100'></div>
            <div className=''>
            <FormLabel>Custom password</FormLabel>
            <InputGroup style={{width:fieldSize}} className="">
              <Form.Control id="shortenPass" aria-label="link" placeholder='custom password' type="text" value={resultPassword} readOnly={true} />
              <InputGroup.Text onClick={(e)=>{writeClipboard("shortenUrl");}}><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M360-240q-33 0-56.5-23.5T280-320v-480q0-33 23.5-56.5T360-880h360q33 0 56.5 23.5T800-800v480q0 33-23.5 56.5T720-240H360Zm0-80h360v-480H360v480ZM200-80q-33 0-56.5-23.5T120-160v-560h80v560h440v80H200Zm160-240v-480 480Z"/></svg>
              </InputGroup.Text>
            </InputGroup>
            </div>
            <div className='w-100'></div>
            <Button onClick={(e)=>{setPopupActive(!popupActive);}}>Close</Button>
          </div>
        </div>
      </div>}
      <div id="mainwindow">
        {(!createMode && !editMode && !deleteMode ) && <>
        <h1 className='text-center'>URL shortener</h1>
        <p className='text-center'>Choose what would you like to do:</p>
        <div className='center'>
        <ButtonGroup id="groupbuttons">
          <Button onClick={(e)=>{setCreateMode(!createMode);}}>Create</Button>
          <Button onClick={(e)=>{setEditMode(!editMode);}} variant='secondary'>Edit</Button>
          <Button onClick={(e)=>{setDeleteMode(!deleteMode);}} variant='danger'>Delete</Button>
        </ButtonGroup>
        </div></>}
        {(createMode || editMode || deleteMode) && <Button onClick={(e)=>{back();}}>Back</Button>}

        {createMode && <>
          <h2 className='text-center'>Create short URL</h2>
          <div className='center justify-content-around'>
            <div className=''>
            <FormLabel>Source link</FormLabel>
            <InputGroup style={{width:fieldSize}} className="">
              <InputGroup.Text><svg xmlns="http://www.w3.org/2000/svg" height="100%" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M440-280H280q-83 0-141.5-58.5T80-480q0-83 58.5-141.5T280-680h160v80H280q-50 0-85 35t-35 85q0 50 35 85t85 35h160v80ZM320-440v-80h320v80H320Zm200 160v-80h160q50 0 85-35t35-85q0-50-35-85t-85-35H520v-80h160q83 0 141.5 58.5T880-480q0 83-58.5 141.5T680-280H520Z"/></svg></InputGroup.Text>
              <Form.Control aria-label="link" placeholder='https://...' type="text" value={newLink} onInput={(e)=>{setNewLink(e.target.value);}}/>
            </InputGroup>
            </div>
            <div className=''>
            <FormLabel>Custom link</FormLabel>
            <InputGroup style={{width:fieldSize}} className="">
              <InputGroup.Text><svg height="24px" viewBox="0 0 24 24" fill="#e8eaed" xmlns="http://www.w3.org/2000/svg"><path d="M16 3L8 21" stroke="#e8eaed" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg></InputGroup.Text>
              <Form.Control aria-label="link" placeholder='alias (optional)' type="text" value={newAlias} onInput={(e)=>{setNewAlias(e.target.value);}}/>
            </InputGroup>
            </div>
            <div className=''>
            <FormLabel>Custom password</FormLabel>
            <InputGroup style={{width:fieldSize}} className="">
              <InputGroup.Text><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M240-80q-33 0-56.5-23.5T160-160v-400q0-33 23.5-56.5T240-640h40v-80q0-83 58.5-141.5T480-920q83 0 141.5 58.5T680-720v80h40q33 0 56.5 23.5T800-560v400q0 33-23.5 56.5T720-80H240Zm0-80h480v-400H240v400Zm240-120q33 0 56.5-23.5T560-360q0-33-23.5-56.5T480-440q-33 0-56.5 23.5T400-360q0 33 23.5 56.5T480-280ZM360-640h240v-80q0-50-35-85t-85-35q-50 0-85 35t-35 85v80ZM240-160v-400 400Z"/></svg></InputGroup.Text>
              <Form.Control aria-label="link" placeholder='custom password (optional)' type="text" value={newPassword} onInput={(e)=>{setNewPassword(e.target.value);}}/>
            </InputGroup>
            </div>
            <hr className='w-100'></hr>
            <Button onClick={(e)=>{submit();}} disabled={isButtonDisabled}>Submit</Button>
          </div>
          
        </>}

        <div className='center justify-content-around'>
            {responseMessage && 
              <Alert variant={isSuccess ? "success" : "danger"} dismissible={true} onClose={() => setResponseMessage("")}>
                {responseMessage}
              </Alert>
            }
          </div>
      </div>
    </div>
  );
}
document.body.setAttribute("data-bs-theme","dark")
export default App;
