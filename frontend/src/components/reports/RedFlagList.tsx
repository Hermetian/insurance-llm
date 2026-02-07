import { useState } from 'react'

interface RedFlag {
  name: string
  severity: 'dealbreaker' | 'critical' | 'warning' | 'minor' | 'boilerplate'
  clause_text?: string
  explanation: string
  protection?: string
  what_to_ask?: string
}

interface RedFlagListProps {
  flags: RedFlag[]
  protectionLabel?: string
}

export default function RedFlagList({ flags, protectionLabel = 'PROTECTION' }: RedFlagListProps) {
  const [boilerplateOpen, setBoilerplateOpen] = useState(false)

  // Normalize legacy 'info' severity to 'minor'
  const normalized = flags.map(f => ({
    ...f,
    severity: (f.severity === 'info' ? 'minor' : f.severity) as RedFlag['severity']
  }))

  const dealbreakers = normalized.filter(rf => rf.severity === 'dealbreaker')
  const criticalFlags = normalized.filter(rf => rf.severity === 'critical')
  const warningFlags = normalized.filter(rf => rf.severity === 'warning')
  const minorFlags = normalized.filter(rf => rf.severity === 'minor')
  const boilerplateFlags = normalized.filter(rf => rf.severity === 'boilerplate')

  return (
    <>
      {dealbreakers.length > 0 && (
        <div className="data-card dealbreaker full-width">
          <h3>!!! DEALBREAKERS - DO NOT SIGN</h3>
          <div className="compliance-items">
            {dealbreakers.map((flag, i) => (
              <div key={i} className="compliance-item dealbreaker">
                <div className="item-header">
                  <span className="status-icon">&#9760;</span>
                  <span className="item-name">{flag.name}</span>
                </div>
                {flag.clause_text && (
                  <div className="clause-text">
                    <span className="label">CLAUSE:</span>
                    <span className="value">&quot;{flag.clause_text}&quot;</span>
                  </div>
                )}
                <p className="item-explanation">{flag.explanation}</p>
                <div className="protection-box">
                  <span className="label">{protectionLabel}:</span>
                  <span className="value">{flag.protection || flag.what_to_ask}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {criticalFlags.length > 0 && (
        <div className="data-card danger full-width">
          <h3>XX CRITICAL RED FLAGS</h3>
          <div className="compliance-items">
            {criticalFlags.map((flag, i) => (
              <div key={i} className="compliance-item fail">
                <div className="item-header">
                  <span className="status-icon">&#10007;</span>
                  <span className="item-name">{flag.name}</span>
                </div>
                {flag.clause_text && (
                  <div className="clause-text">
                    <span className="label">CLAUSE:</span>
                    <span className="value">&quot;{flag.clause_text}&quot;</span>
                  </div>
                )}
                <p className="item-explanation">{flag.explanation}</p>
                <div className="protection-box">
                  <span className="label">{protectionLabel}:</span>
                  <span className="value">{flag.protection || flag.what_to_ask}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {warningFlags.length > 0 && (
        <div className="data-card warning full-width">
          <h3>!! WATCH OUT FOR</h3>
          <div className="compliance-items">
            {warningFlags.map((flag, i) => (
              <div key={i} className="compliance-item warning">
                <div className="item-header">
                  <span className="status-icon">!</span>
                  <span className="item-name">{flag.name}</span>
                </div>
                {flag.clause_text && (
                  <div className="clause-text">
                    <span className="label">CLAUSE:</span>
                    <span className="value">&quot;{flag.clause_text}&quot;</span>
                  </div>
                )}
                <p className="item-explanation">{flag.explanation}</p>
                <div className="protection-box">
                  <span className="label">{protectionLabel}:</span>
                  <span className="value">{flag.protection || flag.what_to_ask}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {minorFlags.length > 0 && (
        <div className="data-card minor full-width">
          <h3>-- MINOR NOTES</h3>
          <div className="compliance-items">
            {minorFlags.map((flag, i) => (
              <div key={i} className="compliance-item minor">
                <div className="item-header">
                  <span className="status-icon">-</span>
                  <span className="item-name">{flag.name}</span>
                </div>
                {flag.clause_text && (
                  <div className="clause-text">
                    <span className="label">CLAUSE:</span>
                    <span className="value">&quot;{flag.clause_text}&quot;</span>
                  </div>
                )}
                <p className="item-explanation">{flag.explanation}</p>
                <div className="protection-box">
                  <span className="label">{protectionLabel}:</span>
                  <span className="value">{flag.protection || flag.what_to_ask}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {boilerplateFlags.length > 0 && (
        <div className="data-card boilerplate full-width">
          <div className="boilerplate-header" onClick={() => setBoilerplateOpen(!boilerplateOpen)} style={{ cursor: 'pointer' }}>
            <h3>[OK] STANDARD CLAUSES ({boilerplateFlags.length} items) {boilerplateOpen ? '[-]' : '[+]'}</h3>
          </div>
          {boilerplateOpen && (
            <div className="compliance-items">
              {boilerplateFlags.map((flag, i) => (
                <div key={i} className="compliance-item boilerplate">
                  <div className="item-header">
                    <span className="status-icon">&#10003;</span>
                    <span className="item-name">{flag.name}</span>
                  </div>
                  <p className="item-explanation">{flag.explanation}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </>
  )
}
