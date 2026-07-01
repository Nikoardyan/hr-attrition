import { useState, useEffect } from 'react'
import axios from 'axios'
import Overview from './Overview'
import PredictForm from './PredictForm'

function App() {
  const [view, setView] = useState('overview')

  return (
    <div className="flex-1 flex flex-col md:flex-row min-h-screen w-full">
      {/* SideNavBar */}
      <nav className="fixed left-0 top-0 h-full z-40 hidden md:flex flex-col py-6 px-4 bg-surface-container dark:bg-surface-container-low backdrop-blur-2xl text-secondary dark:text-secondary shadow-xl border-r border-white/5 w-64">
        {/* Header */}
        <div className="mb-8 px-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-primary-container overflow-hidden border border-white/10 shrink-0">
            <img alt="HR Analytics Lab" className="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBTy5QN2XhfZjhlxu8DwnxFj1DE6hEOoRe0Iv7wyO0xPF_jA5EOvuRT6KMZtZx5HSE4C1LY6zVhd8J8OMizE5KfcDHGla47wRa3quZ7abCp4kZdQI2a4-zUwDNk8CciVWisuVFvNMv47RSyq-9BPGD9OTErwyQqrwIjAzA3764EdgfMaOANwNEGFJYqvr_mtyPqqtgHHBNkArVp-Gzthuf2X4opKFbR7VpBU4HOuhH31SJkzqXDZuCv4HC_QGsQyE4zPKoBaM2pcxw"/>
          </div>
          <div>
            <h1 className="font-headline-sm text-[20px] font-black text-secondary leading-tight">PredictiveHR</h1>
            <p className="font-body-sm text-[12px] text-on-surface-variant opacity-80">AI-Driven Talent Intelligence</p>
          </div>
        </div>

        {/* Main Navigation */}
        <ul className="space-y-2 flex-grow">
          <li>
            <button 
              onClick={() => setView('overview')}
              className={`w-full flex items-center gap-3 rounded-lg px-4 py-3 transition-all ${view === 'overview' ? 'text-secondary bg-secondary/10 scale-95' : 'text-on-surface-variant hover:text-on-surface hover:bg-white/5'}`}
            >
              <span className="material-symbols-outlined">dashboard</span>
              <span className="font-label-md text-[12px]">Overview</span>
            </button>
          </li>
          <li>
            <button 
              onClick={() => setView('predict')}
              className={`w-full flex items-center gap-3 rounded-lg px-4 py-3 transition-all ${view === 'predict' ? 'text-secondary bg-secondary/10 scale-95' : 'text-on-surface-variant hover:text-on-surface hover:bg-white/5'}`}
            >
              <span className="material-symbols-outlined">psychology</span>
              <span className="font-label-md text-[12px]">Predict Risk</span>
            </button>
          </li>
        </ul>
      </nav>

      {/* Main Content Wrapper */}
      <div className="flex-1 md:ml-64 flex flex-col min-h-screen">
        {/* TopNavBar (Mobile) */}
        <header className="fixed top-0 left-0 md:left-64 right-0 z-30 flex justify-between items-center px-4 h-16 bg-surface/70 backdrop-blur-xl text-secondary shadow-sm border-b border-white/10 md:hidden">
          <div className="font-headline-md text-headline-md font-bold text-secondary">PredictiveHR</div>
        </header>

        {/* Dashboard Canvas */}
        <main className="flex-1 p-4 md:p-8 mt-16 md:mt-0 pt-8 max-w-[1440px] mx-auto w-full">
          {view === 'overview' && <Overview />}
          {view === 'predict' && <PredictForm />}
        </main>
      </div>
    </div>
  )
}

export default App
