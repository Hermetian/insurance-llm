import RedFlagList from './RedFlagList'
import LetterView from './LetterView'
import { getRiskColor, getRiskLabel } from './utils'

interface DebtSettlementRedFlag {
  name: string
  severity: 'critical' | 'warning' | 'info'
  clause_text?: string
  explanation: string
  what_to_ask: string
}

interface DebtSettlementContractReport {
  overall_risk: string
  risk_score: number
  company_name?: string
  settlement_type?: string
  has_paid_in_full: boolean
  has_tax_warning: boolean
  resets_statute_of_limitations: boolean
  red_flags: DebtSettlementRedFlag[]
  missing_protections: string[]
  summary: string
  settlement_letter: string
}

interface DebtSettlementReportProps {
  report: DebtSettlementContractReport
  tab: 'report' | 'letter'
  setTab: (tab: 'report' | 'letter') => void
}

export default function DebtSettlementReport({ report, tab, setTab }: DebtSettlementReportProps) {
  return (
    <section className="output-section debt-settlement-output">
      <div className="compliance-header">
        <div
          className="compliance-status-badge"
          style={{ backgroundColor: getRiskColor(report.overall_risk) }}
        >
          {getRiskLabel(report.overall_risk)}
        </div>
        <div className="risk-exposure">
          <span className="label">PAID-IN-FULL:</span>
          <span className="value" style={!report.has_paid_in_full ? { color: '#ff4444' } : undefined}>
            {report.has_paid_in_full ? 'YES' : 'MISSING - DANGER'}
          </span>
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
          * SETTLEMENT LETTER
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
                <span className="label">COMPANY:</span>
                <span className="value">{report.company_name || '---'}</span>
              </div>
              <div className="data-row">
                <span className="label">TYPE:</span>
                <span className="value">{report.settlement_type?.toUpperCase() || '---'}</span>
              </div>
              <div className="data-row">
                <span className="label">PAID IN FULL:</span>
                <span className={`value ${report.has_paid_in_full ? 'pass' : 'fail'}`}>
                  {report.has_paid_in_full ? 'YES' : 'NO'}
                </span>
              </div>
              <div className="data-row">
                <span className="label">TAX WARNING:</span>
                <span className={`value ${report.has_tax_warning ? 'pass' : 'fail'}`}>
                  {report.has_tax_warning ? 'YES' : 'NO'}
                </span>
              </div>
              <div className="data-row">
                <span className="label">SOL RESET:</span>
                <span className={`value ${report.resets_statute_of_limitations ? 'fail' : 'pass'}`}>
                  {report.resets_statute_of_limitations ? 'YES - DANGER' : 'NO'}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {tab === 'letter' && (
        <LetterView text={report.settlement_letter} copyLabel="COPY LETTER" />
      )}
    </section>
  )
}
