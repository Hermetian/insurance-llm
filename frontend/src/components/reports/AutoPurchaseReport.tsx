import RedFlagList from './RedFlagList'
import LetterView from './LetterView'
import { getRiskColor, getRiskLabel } from './utils'

interface AutoPurchaseRedFlag {
  name: string
  severity: 'dealbreaker' | 'critical' | 'warning' | 'minor' | 'boilerplate'
  clause_text?: string
  explanation: string
  what_to_ask: string
}

interface AutoPurchaseContractReport {
  overall_risk: string
  risk_score: number
  dealer_name?: string
  vehicle_description?: string
  financing_type?: string
  has_yoyo_financing: boolean
  total_junk_fees?: string
  red_flags: AutoPurchaseRedFlag[]
  state_protections: string[]
  summary: string
  demand_letter: string
}

interface AutoPurchaseReportProps {
  report: AutoPurchaseContractReport
  tab: 'report' | 'letter'
  setTab: (tab: 'report' | 'letter') => void
}

export default function AutoPurchaseReport({ report, tab, setTab }: AutoPurchaseReportProps) {
  return (
    <section className="output-section auto-purchase-output">
      <div className="compliance-header">
        <div
          className="compliance-status-badge"
          style={{ backgroundColor: getRiskColor(report.overall_risk) }}
        >
          {getRiskLabel(report.overall_risk)}
        </div>
        <div className="risk-exposure">
          <span className="label">JUNK FEES:</span>
          <span className="value">{report.total_junk_fees || 'UNKNOWN'}</span>
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
          * DEMAND LETTER
        </button>
      </div>

      {tab === 'report' && (
        <div className="compliance-report">
          <RedFlagList flags={report.red_flags} />

          {report.state_protections.length > 0 && (
            <div className="data-card success full-width">
              <h3>** YOUR STATE PROTECTIONS</h3>
              <div className="missing-list">
                {report.state_protections.map((item, i) => (
                  <div key={i} className="missing-item">
                    <span className="status-icon">✓</span>
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
                <span className="label">DEALER:</span>
                <span className="value">{report.dealer_name || '---'}</span>
              </div>
              <div className="data-row">
                <span className="label">VEHICLE:</span>
                <span className="value">{report.vehicle_description || '---'}</span>
              </div>
              <div className="data-row">
                <span className="label">FINANCING:</span>
                <span className="value">{report.financing_type?.toUpperCase() || '---'}</span>
              </div>
              <div className="data-row">
                <span className="label">YO-YO:</span>
                <span className={`value ${report.has_yoyo_financing ? 'fail' : 'pass'}`}>
                  {report.has_yoyo_financing ? 'YES - DANGER' : 'NO'}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {tab === 'letter' && (
        <LetterView text={report.demand_letter} copyLabel="COPY LETTER" />
      )}
    </section>
  )
}
