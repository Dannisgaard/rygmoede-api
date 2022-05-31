import React from 'react'
import {Route , Routes} from 'react-router-dom';
import Home from '../pages/Home'
import Photo from '../pages/Photo';

const AuthRouter = () => {
    return (
        <Routes>
            <Route path="/" element={<Home/>}/>
            <Route path="/photo/get_photo/:id" element={<Photo/>}/>
        </Routes>
    )
}

export default AuthRouter
