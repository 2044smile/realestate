import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

const App = () => {
  return (
    <div className="h-screen flex flex-col">
      <header className="bg-purple-700 text-white text-center py-4 text-2xl font-bold w-full fixed top-0 left-0">
        스마트매물찾기
      </header>

      <main className="flex-grow flex items-center justify-center p-4">
        <div className="hidden md:block text-center text-gray-700 text-xl">
          메인 화면
        </div>
        <div className="md:hidden text-center text-gray-700 text-xl">
          모바일 화면
        </div>
      </main>

      <footer className="bg-gray-800 text-white text-center py-2 text-sm w-full fixed bottom-0 left-0">
        2025 스마트매물찾기. All rights reserved
      </footer>
    </div>
  )
}

export default App
