import RedFlagList from './RedFlagList'
import LetterView from './LetterView'
import { getRiskColor, getRiskLabel } from './utils'

interface HomeImprovementRedFlag {
  name: string
  severity: 'critical' | 'warning' | 'info'
  clause_text?: string
  explanation: string
  what_to_ask: string
}

interface HomeImprovementContractReport {
  overall_risk: string
  risk_score: number
  contractor_name?: string
  project_type?: string
  payment_structure?: string
  has_lien_waiver: boolean
  has_change_order_process: boolean
  red_flags: HomeImprovementRedFlag[]
  missing_protections: string[]
  summary: string
  protection_checklist: string
}

interface HomeImprovementReportProps {
  report: HomeImprovementContractReport
  tab: 'report' | 'letter'
  setTab: (tab: 'report' | 'letter') => void
}

export default function HomeImprovementReport({ report, tab, setTab }: HomeImprovementReportProps) {
  return (
    <section className="output-section home-improvement-output">
      <div className="compliance-header">
        <div
          className="compliance-status-badge"
          style={{ backgroundColor: getRiskColor(report.overall_risk) }}
        >
          {getRiskLabel(report.overall_risk)}
        </div>
        <div className="risk-exposure">
          <span className="label">PAYMENT RISK:</span>
          <span className="value">{report.payment_structure || 'UNKNOWN'}</span>
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
          * PROTECTION CHECKLIST
        </button>
      </div>

      {tab === 'report' && (
        <div className="compliance-report">
          <RedFlagList flags={report.red_flags} />

          {report.missing_protections.length > 0 && (
            <div className="data-card warning full-width">
              <h3>!! MISSING PROTECTIONS</h3>
              <div className="missing-list">
                {report.missing_protections.map((item, i) => (
                  <div key={i} className="missing-item">
                    <span className="status-icon">&#10007;</span>
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
                <span className="label">CONTRACTOR:</span>
                <span className="value">{report.contractor_name || '---'}</span>
              </div>
              <div className="data-row">
                <span className="label">PROJECT:</span>
                <span className="value">{report.project_type?.toUpperCase() || '---'}</span>
              </div>
              <div className="data-row">
                <span className="label">LIEN WAIVER:</span>
                <span className={`value ${report.has_lien_waiver ? 'pass' : 'fail'}`}>
                  {report.has_lien_waiver ? 'YES' : 'NO'}
                </span>
              </div>
              <div className="data-row">
                <span className="label">CHANGE ORDERS:</span>
                <span className={`value ${report.has_change_order_process ? 'pass' : 'fail'}`}>
                  {report.has_change_order_process ? 'YES' : 'NO'}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {tab === 'letter' && (
        <LetterView text={report.protection_checklist} copyLabel="COPY CHECKLIST" />
      )}
    </section>
  )
}
