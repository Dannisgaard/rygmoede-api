import {React , useState} from 'react'
import image from '../assets/image.svg'
import "../styles/Home.css"
import { server } from '../context/Api';
import axios  from 'axios';
import ProgresBar  from '../components/ProgresBar';
import { useNavigate }  from "react-router-dom"
const Home = () => {

    const [file ,setFile] = useState('');
    const [ show, setShow ] = useState(false)
    const navigate = useNavigate();

    const  dragover_handler = ( ev ) => {
        ev.preventDefault();
        ev.dataTransfer.dropEffect = "move";
        console.log("dragover")
    }
    const drop_handler = (e) => {
        const file = e.dataTransfer.files[0];
        e.preventDefault();
        send(file)
    }
    const send = (file) => {
        const formData = new FormData();
        formData.append('image', file);
        axios.post(`${server}/photo/upload`, formData , {
            mode: 'no-cors',
            onUploadProgress: () => {
                setShow(true)
            }
        }).then(res => {
            setShow(false)
            if  (res.status === 201) {
                navigate(`/photo/get_photo/${res.data.id}`)
            }
        }).catch(err => {
            console.log(err)
        });
    }

    return (
        <div>
            <div className="imageContainer">
                <h1>Upload your image</h1>
                <h3>File should be Jpeg, Png...</h3>
                <ProgresBar show={show} />
                <form action="" method='POST' >
                    <div id="test" onDrop={(e) => drop_handler(e)} name="file"  onDragOver={(ev) => dragover_handler(ev)} className='uploadImage' >
                            <img src={image} alt="" />
                        <h2>Drag & Drop your image here </h2>
                    </div>
                    <h3>Or</h3>
                    <label htmlFor="file" className='file-upload' >Choose file</label>
                    <input id="file" type="file" name="file" onChange={() => {
                        const file = document.getElementById('file').files[0];
                        setFile(file)
                        send(file)
                    }} />
                </form>
            </div>
        </div>
    )
}

export default Home
