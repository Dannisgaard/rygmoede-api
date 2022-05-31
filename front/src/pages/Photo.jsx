import {React, useEffect, useState} from 'react'
import checkIcon from '../assets/checkIcon.png'
import axios from 'axios';
import '../styles/Photo.css'
import { server } from '../context/Api';
import { useParams } from 'react-router-dom';


const Photo = () => {
    const [image,setImage] = useState('');
    const [loading,setLoading] = useState(true);


    let {id} = useParams();
    useEffect(() => {
        console.log("iniciando fetch")
        setLoading(true)
        axios.get(`${server}/photo/get_photo/${id}`).then(res => {
            setImage(res.data)
        }).catch(err => {
            console.log(err)
        })
    },[id])

    setTimeout(() => {
        setLoading(false)
    },1000)


    return(loading ? <div className="loading">
            loading
        </div> : (
        <div>
            <div className = 'photoUploadedContainer'>
                <img src = {checkIcon} alt = "" />
                <h2>Uploaded Successfully!</h2>
                <div className='uploadContainer'>
                    <img
                            src={`${server}/photo/image/${id}`}
                    alt="" />
                </div>
                <div className='copyLinkContainer'>
                    <div className='textContainer'>
                            <input defaultValue={`${server}/photo/image/${id}`}/>
                        <button className="copyLinkButton" onClick={() => {
                                navigator.clipboard.writeText( `${server}/photo/image/${ id }`)}
                            }>Copy Link</button>
                    </div>
                </div>
            </div >
        </div >
        )
    )
}

export default Photo
