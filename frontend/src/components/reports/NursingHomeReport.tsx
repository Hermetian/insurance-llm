import RedFlagList from './RedFlagList'
import LetterView from './LetterView'
import { getRiskColor, getRiskLabel } from './utils'

interface NursingHomeRedFlag {
  name: string
  severity: 'dealbreaker' | 'critical' | 'warning' | 'minor' | 'boilerplate'
  clause_text?: string
  explanation: string
  what_to_ask: string
}

interface NursingHomeContractReport {
  overall_risk: string
  risk_score: number
  facility_name?: string
  agreement_type?: string
  has_responsible_party_clause: boolean
  has_forced_arbitration: boolean
  has_liability_waiver: boolean
  illegal_clauses: string[]
  red_flags: NursingHomeRedFlag[]
  summary: string
  rights_guide: string
}

interface NursingHomeReportProps {
  report: NursingHomeContractReport
  tab: 'report' | 'letter'
  setTab: (tab: 'report' | 'letter') => void
}

export default function NursingHomeReport({ report, tab, setTab }: NursingHomeReportProps) {
  return (
    <section className="output-section nursing-home-output">
      <div className="compliance-header">
        <div
          className="compliance-status-badge"
          style={{ backgroundColor: getRiskColor(report.overall_risk) }}
        >
          {getRiskLabel(report.overall_risk)}
        </div>
        <div className="risk-exposure">
          <span className="label">ILLEGAL CLAUSES:</span>
          <span className="value">{report.illegal_clauses.length}</span>
        </div>
      </div>

      <p className="summary-text">{report.summary}</p>

      <div className="tabs">
        <button
          className={`tab ${tab === 'report' ? 'active' : ''}`}
          onClick={() => setTab('report')}
        >
          * ANALYSIS
        </button>
        <button
          className={`tab ${tab === 'letter' ? 'active' : ''}`}
          onClick={() => setTab('letter')}
        >
          * RIGHTS GUIDE
        </button>
      </div>

      {tab === 'report' && (
        <div className="compliance-report">
          <RedFlagList flags={report.red_flags} />

          {report.illegal_clauses.length > 0 && (
            <div className="data-card danger full-width">
              <h3>!! ILLEGAL CLAUSES</h3>
              <div className="missing-list">
                {report.illegal_clauses.map((item, i) => (
                  <div key={i} className="missing-item">
                    <span className="status-icon">!!</span>
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="data-card full-width">
            <h3>* CONTRACT INFO</h3>
            <div className="coi-data-grid">
              <div className="data-row">
                <span className="label">FACILITY:</span>
                <span className="value">{report.facility_name || '---'}</span>
              </div>
              <div className="data-row">
                <span className="label">TYPE:</span>
                <span className="value">{report.agreement_type?.toUpperCase() || '---'}</span>
              </div>
              <div className="data-row">
                <span className="label">RESPONSIBLE PARTY:</span>
                <span className={`value ${report.has_responsible_party_clause ? 'fail' : 'pass'}`}>
                  {report.has_responsible_party_clause ? 'YES - ILLEGAL' : 'NO'}
                </span>
              </div>
              <div className="data-row">
                <span className="label">FORCED ARBITRATION:</span>
                <span className={`value ${report.has_forced_arbitration ? 'fail' : 'pass'}`}>
                  {report.has_forced_arbitration ? 'YES' : 'NO'}
                </span>
              </div>
              <div className="data-row">
                <span className="label">LIABILITY WAIVER:</span>
                <span className={`value ${report.has_liability_waiver ? 'fail' : 'pass'}`}>
                  {report.has_liability_waiver ? 'YES' : 'NO'}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {tab === 'letter' && (
        <LetterView text={report.rights_guide} copyLabel="COPY GUIDE" />
      )}
    </section>
  )
}
