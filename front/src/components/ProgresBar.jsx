import React from 'react'
import {Modal} from 'react-bootstrap'
import '../styles/modal.css'

const ProgresBar = ({show}) => {
    
    return (
        <Modal show={show} >
                <div className="modalProgres">
                    <h2>Uploading ...</h2>
                    <div className='loader-bar'>
                        <div className='loader-blue'></div>
                    </div>
                </div>
            </Modal>
    )
}

export default ProgresBar
