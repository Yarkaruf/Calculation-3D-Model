import type { NextPage } from 'next'
import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'

const Home: NextPage = () => {
  function fileLoad (e:any){
    const file = e.target.files[0];
    const data = new FormData();
    data.append('file', file);
    filePost(data)
}
function filePost(data:any){
  fetch("http://127.0.0.1:5000/analyze",{
    method:"POST",
    body: data,
  })
  .then(function(response){
    return response.json()
  })
  // .then(function(data){ // use different name to avoid confusion
  .then(function(res){
    console.log('success')
    console.log(res)
  })
}
  return (
    <form>
      <input onChange={fileLoad} type='file' />
      <input onClick={filePost} type='button' value='отправить'/>
    </form>
  )
}

export default Home
