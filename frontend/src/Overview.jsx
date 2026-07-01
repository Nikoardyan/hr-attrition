import { useState, useEffect } from 'react'
import axios from 'axios'

export default function Overview() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    // We can fetch data here from API
    // axios.get('http://localhost:8000/predictions').then(...)
  }, [])

  return (
    <>
      <header className="mb-section-margin flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h2 className="font-headline-lg text-[32px] font-bold text-on-surface mb-2">Workforce Attrition Overview</h2>
          <p className="font-body-lg text-[16px] text-on-surface-variant">Real-time predictive analysis for the next 6 months.</p>
        </div>
        <div className="flex gap-2">
          <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-surface-container-high border border-outline-variant font-label-md text-[12px] text-on-surface-variant">
            <span className="w-2 h-2 rounded-full bg-secondary glow-accent"></span> Live Sync
          </span>
        </div>
      </header>

      {/* Bento Grid Layout */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-4">
        
        {/* Hero Statistic Card */}
        <div className="glass-card rounded-xl p-[1.5rem] md:col-span-4 flex flex-col justify-between relative overflow-hidden group hover:border-secondary/30 transition-colors">
          <div className="absolute top-0 right-0 w-32 h-32 bg-secondary/10 rounded-full blur-3xl -mr-10 -mt-10 pointer-events-none"></div>
          <div>
            <h3 className="font-label-md text-[12px] text-on-surface-variant uppercase tracking-wider mb-4 flex items-center gap-2">
              <span className="material-symbols-outlined text-[16px] text-secondary">trending_up</span> Total Attrition Risk
            </h3>
            <div className="flex items-baseline gap-3 mb-2">
              <span className="font-data-display text-[40px] font-bold text-on-surface">18.4%</span>
              <span className="font-body-md text-[14px] text-error flex items-center">
                <span className="material-symbols-outlined text-[14px]">arrow_upward</span> 2.1%
              </span>
            </div>
            <p className="font-body-sm text-[12px] text-on-surface-variant">Projected turnover rate by end of Q4</p>
          </div>
          <div className="mt-6 pt-6 border-t border-white/5">
            <div className="flex justify-between items-center mb-2">
              <span className="font-label-md text-[12px] text-on-surface-variant">Risk Level Indicator</span>
              <span className="font-label-md text-[12px] text-error px-2 py-0.5 bg-error/10 rounded">HIGH</span>
            </div>
            <div className="w-full bg-surface-container h-2 rounded-full overflow-hidden">
              <div className="bg-error h-full rounded-full" style={{ width: '75%' }}></div>
            </div>
          </div>
        </div>

        {/* AI Insights Panel */}
        <div className="glass-card rounded-xl p-[1.5rem] md:col-span-4 flex flex-col">
          <h3 className="font-label-md text-[12px] text-on-surface-variant uppercase tracking-wider mb-6 flex items-center gap-2">
            <span className="material-symbols-outlined text-[16px] text-secondary">psychology</span> Top Risk Factors
          </h3>
          <div className="space-y-4 flex-grow">
            <div className="flex items-start gap-3 p-3 bg-surface-container/50 rounded-lg border border-white/5">
              <div className="w-8 h-8 rounded-full bg-error/10 flex items-center justify-center shrink-0 text-error">1</div>
              <div>
                <h4 className="font-body-md text-[14px] font-semibold text-on-surface mb-1">Work-Life Balance</h4>
                <p className="font-body-sm text-[12px] text-on-surface-variant">65% of high-risk cohort report sustained over-utilization.</p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-3 bg-surface-container/50 rounded-lg border border-white/5">
              <div className="w-8 h-8 rounded-full bg-tertiary/10 flex items-center justify-center shrink-0 text-tertiary">2</div>
              <div>
                <h4 className="font-body-md text-[14px] font-semibold text-on-surface mb-1">Compensation Ratio</h4>
                <p className="font-body-sm text-[12px] text-on-surface-variant">Engineering dept comp-ratios fell below market median.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Actionable Recommendations */}
        <div className="glass-card rounded-xl p-[1.5rem] md:col-span-4 bg-surface-bright/20 flex flex-col">
          <h3 className="font-label-md text-[12px] text-on-surface-variant uppercase tracking-wider mb-6 flex items-center gap-2">
            <span className="material-symbols-outlined text-[16px] text-secondary">lightbulb</span> AI Recommendations
          </h3>
          <ul className="space-y-3 flex-grow">
            <li className="p-3 bg-surface/40 rounded border-l-2 border-secondary flex flex-col gap-2">
              <span className="font-body-sm text-[14px] font-semibold text-on-surface">Initiate Stay Interviews</span>
              <span className="font-body-sm text-[12px] text-on-surface-variant">Target Top Performers in Engineering (Tenure &gt; 2yrs).</span>
            </li>
            <li className="p-3 bg-surface/40 rounded border-l-2 border-tertiary flex flex-col gap-2">
              <span className="font-body-sm text-[14px] font-semibold text-on-surface">Comp Review Cycle</span>
              <span className="font-body-sm text-[12px] text-on-surface-variant">Accelerate mid-year adjustments for high-flight-risk roles.</span>
            </li>
          </ul>
        </div>
      </div>
    </>
  )
}
