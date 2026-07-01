import { useState } from 'react'
import axios from 'axios'

const DEFAULTS = {
  Age: 35, Gender: "Male", MaritalStatus: "Single", Education: 3, EducationField: "Life Sciences", DistanceFromHome: 5,
  Department: "Research & Development", JobRole: "Laboratory Technician", JobLevel: 2, BusinessTravel: "Travel_Rarely", OverTime: "No", NumCompaniesWorked: 2, TotalWorkingYears: 10,
  MonthlyIncome: 5000, DailyRate: 800, HourlyRate: 65, MonthlyRate: 14000, PercentSalaryHike: 15, StockOptionLevel: 0, YearsAtCompany: 5, YearsInCurrentRole: 3, YearsSinceLastPromotion: 1, YearsWithCurrManager: 3,
  JobSatisfaction: 3, EnvironmentSatisfaction: 3, RelationshipSatisfaction: 3, JobInvolvement: 3, WorkLifeBalance: 3, PerformanceRating: 3, TrainingTimesLastYear: 2
}

export default function PredictForm() {
  const [formData, setFormData] = useState(DEFAULTS)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: isNaN(value) || value === '' ? value : Number(value) }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      // Hit FastAPI
      const res = await axios.post('http://localhost:8000/explain', formData)
      setResult(res.data)
    } catch (err) {
      alert("Error: Make sure the API is running at localhost:8000")
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2 className="font-headline-lg text-[32px] font-bold text-on-surface mb-6">Predict Employee Risk</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-8 glass-card p-6 rounded-xl">
          <form onSubmit={handleSubmit} className="space-y-6">
            
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-[12px] text-on-surface-variant mb-1">Age</label>
                <input type="number" name="Age" value={formData.Age} onChange={handleChange} className="w-full bg-surface-container border border-outline-variant rounded px-3 py-2 text-on-surface text-[14px]" />
              </div>
              <div>
                <label className="block text-[12px] text-on-surface-variant mb-1">Gender</label>
                <select name="Gender" value={formData.Gender} onChange={handleChange} className="w-full bg-surface-container border border-outline-variant rounded px-3 py-2 text-on-surface text-[14px]">
                  <option>Male</option><option>Female</option>
                </select>
              </div>
              <div>
                <label className="block text-[12px] text-on-surface-variant mb-1">Marital Status</label>
                <select name="MaritalStatus" value={formData.MaritalStatus} onChange={handleChange} className="w-full bg-surface-container border border-outline-variant rounded px-3 py-2 text-on-surface text-[14px]">
                  <option>Single</option><option>Married</option><option>Divorced</option>
                </select>
              </div>
              <div>
                <label className="block text-[12px] text-on-surface-variant mb-1">Department</label>
                <select name="Department" value={formData.Department} onChange={handleChange} className="w-full bg-surface-container border border-outline-variant rounded px-3 py-2 text-on-surface text-[14px]">
                  <option>Sales</option><option>Research & Development</option><option>Human Resources</option>
                </select>
              </div>
              <div>
                <label className="block text-[12px] text-on-surface-variant mb-1">Job Role</label>
                <select name="JobRole" value={formData.JobRole} onChange={handleChange} className="w-full bg-surface-container border border-outline-variant rounded px-3 py-2 text-on-surface text-[14px]">
                  <option>Sales Executive</option><option>Research Scientist</option><option>Laboratory Technician</option><option>Manufacturing Director</option><option>Healthcare Representative</option><option>Manager</option><option>Sales Representative</option><option>Research Director</option><option>Human Resources</option>
                </select>
              </div>
              <div>
                <label className="block text-[12px] text-on-surface-variant mb-1">Monthly Income ($)</label>
                <input type="number" name="MonthlyIncome" value={formData.MonthlyIncome} onChange={handleChange} className="w-full bg-surface-container border border-outline-variant rounded px-3 py-2 text-on-surface text-[14px]" />
              </div>
            </div>

            {/* A few more fields for demo - we would add all 30 fields here */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <label className="block text-[12px] text-on-surface-variant mb-1">OverTime</label>
                <select name="OverTime" value={formData.OverTime} onChange={handleChange} className="w-full bg-surface-container border border-outline-variant rounded px-3 py-2 text-on-surface text-[14px]">
                  <option>Yes</option><option>No</option>
                </select>
              </div>
              <div>
                <label className="block text-[12px] text-on-surface-variant mb-1">Years At Company</label>
                <input type="number" name="YearsAtCompany" value={formData.YearsAtCompany} onChange={handleChange} className="w-full bg-surface-container border border-outline-variant rounded px-3 py-2 text-on-surface text-[14px]" />
              </div>
              <div>
                <label className="block text-[12px] text-on-surface-variant mb-1">Job Satisfaction</label>
                <select name="JobSatisfaction" value={formData.JobSatisfaction} onChange={handleChange} className="w-full bg-surface-container border border-outline-variant rounded px-3 py-2 text-on-surface text-[14px]">
                  <option value={1}>1 (Low)</option><option value={2}>2</option><option value={3}>3</option><option value={4}>4 (High)</option>
                </select>
              </div>
              <div>
                <label className="block text-[12px] text-on-surface-variant mb-1">Work-Life Balance</label>
                <select name="WorkLifeBalance" value={formData.WorkLifeBalance} onChange={handleChange} className="w-full bg-surface-container border border-outline-variant rounded px-3 py-2 text-on-surface text-[14px]">
                  <option value={1}>1 (Low)</option><option value={2}>2</option><option value={3}>3</option><option value={4}>4 (High)</option>
                </select>
              </div>
            </div>

            <button type="submit" disabled={loading} className="w-full py-3 bg-secondary text-surface font-bold rounded hover:bg-secondary-container transition-colors disabled:opacity-50 mt-6">
              {loading ? 'Analyzing...' : 'Analyze Risk Factors'}
            </button>
          </form>
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-4">
          {result ? (
            <div className={`glass-card p-6 rounded-xl ${result.risk_level === 'High' ? 'border-t-error' : result.risk_level === 'Medium' ? 'border-t-tertiary' : 'border-t-secondary'} border-t-[3px]`}>
              <h3 className="text-[14px] text-on-surface-variant uppercase tracking-wider mb-2">Prediction</h3>
              <div className="text-[32px] font-bold text-on-surface mb-4">
                {result.prediction === "Will Leave" ? <span className="text-error">At Risk ({Math.round(result.probability * 100)}%)</span> : <span className="text-secondary">Stable ({Math.round(result.probability * 100)}%)</span>}
              </div>
              
              <div className="mb-6 p-4 bg-surface-container rounded border border-white/5">
                <h4 className="text-[12px] font-bold text-on-surface mb-1">AI Recommendation</h4>
                <p className="text-[14px] text-on-surface-variant">{result.recommendation}</p>
              </div>

              <h4 className="text-[14px] font-bold text-on-surface border-b border-white/10 pb-2 mb-3">Key Drivers</h4>
              <div className="space-y-3">
                {result.contributions.map((c, i) => (
                  <div key={i} className="flex justify-between items-center">
                    <span className="text-[14px] text-on-surface-variant">{c.label} ({c.input})</span>
                    <span className={`text-[12px] px-2 py-0.5 rounded ${c.direction === 'naik' ? 'bg-error/20 text-error' : 'bg-secondary/20 text-secondary'}`}>
                      {c.direction === 'naik' ? '↑ Risk' : '↓ Retain'}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="glass-card p-6 rounded-xl h-full flex flex-col items-center justify-center text-center opacity-50">
              <span className="material-symbols-outlined text-[48px] text-on-surface-variant mb-4">analytics</span>
              <p className="text-on-surface-variant">Fill out the profile and run the analysis to see SHAP explainability insights here.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
