import RedFlagList from './RedFlagList'
import LetterView from './LetterView'
import { getRiskColor, getRiskLabel } from './utils'

interface SubscriptionRedFlag {
  name: string
  severity: 'dealbreaker' | 'critical' | 'warning' | 'minor' | 'boilerplate'
  clause_text?: string
  explanation: string
  what_to_ask: string
}

interface SubscriptionContractReport {
  overall_risk: string
  risk_score: number
  service_name?: string
  subscription_type?: string
  cancellation_difficulty: string
  has_auto_renewal: boolean
  has_price_increase_clause: boolean
  red_flags: SubscriptionRedFlag[]
  dark_patterns: string[]
  summary: string
  cancellation_guide: string
}

interface SubscriptionReportProps {
  report: SubscriptionContractReport
  tab: 'report' | 'letter'
  setTab: (tab: 'report' | 'letter') => void
}

export default function SubscriptionReport({ report, tab, setTab }: SubscriptionReportProps) {
  return (
    <section className="output-section subscription-output">
      <div className="compliance-header">
        <div
          className="compliance-status-badge"
          style={{ backgroundColor: getRiskColor(report.overall_risk) }}
        >
          {getRiskLabel(report.overall_risk)}
        </div>
        <div className="risk-exposure">
          <span className="label">CANCEL DIFFICULTY:</span>
          <span className="value">{report.cancellation_difficulty.toUpperCase()}</span>
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
          * CANCELLATION GUIDE
        </button>
      </div>

      {tab === 'report' && (
        <div className="compliance-report">
          <RedFlagList flags={report.red_flags} />

          {report.dark_patterns.length > 0 && (
            <div className="data-card warning full-width">
              <h3>!! DARK PATTERNS</h3>
              <div className="missing-list">
                {report.dark_patterns.map((item, i) => (
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
                <span className="label">SERVICE:</span>
                <span className="value">{report.service_name || '---'}</span>
              </div>
              <div className="data-row">
                <span className="label">TYPE:</span>
                <span className="value">{report.subscription_type?.toUpperCase() || '---'}</span>
              </div>
              <div className="data-row">
                <span className="label">AUTO-RENEWAL:</span>
                <span className={`value ${report.has_auto_renewal ? 'fail' : 'pass'}`}>
                  {report.has_auto_renewal ? 'YES' : 'NO'}
                </span>
              </div>
              <div className="data-row">
                <span className="label">PRICE INCREASES:</span>
                <span className={`value ${report.has_price_increase_clause ? 'fail' : 'pass'}`}>
                  {report.has_price_increase_clause ? 'YES' : 'NO'}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {tab === 'letter' && (
        <LetterView text={report.cancellation_guide} copyLabel="COPY GUIDE" />
      )}
    </section>
  )
}
