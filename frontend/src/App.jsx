import { useState } from 'react'
import URLCard from './components/UrlCard.jsx'
import URLResults from './components/UrlResults.js'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './css/App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <h1>Short.ly - URL Shortener</h1>
      </div>
      <div>
        <Text text="Welcome to Short.ly! Your go-to solution for quick and easy URL shortening." />
        <Text text="Paste your long URLs below to generate concise, shareable links in an instant." />
        <URLCard originalUrl="https://www.example.com/some/very/long/url" shortUrl="https://short.ly/abc123" />
      </div>
    </>
  )
}

function Text({text}){
  return <p>{text}</p>
}

export default App
