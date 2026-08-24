import { Link } from "react-router-dom"

export default function AuthLayout({ title, description, children, footerText, footerLink, footerLinkText }) {
  return (
    <main className="auth-page">
      <section className="auth-intro" aria-label="StayHub 소개">
        <Link to="/" className="brand">stay<span>hub</span></Link>
        <div className="intro-copy">
          <p className="eyebrow">YOUR NEXT STAY</p>
          <h1>머물고 싶은<br />모든 순간을 찾으세요.</h1>
          <p>편안한 여행의 시작, StayHub와 함께하세요.</p>
        </div>
        <div className="intro-decoration decoration-one" />
        <div className="intro-decoration decoration-two" />
      </section>

      <section className="auth-content">
        <div className="auth-card">
          <Link to="/" className="brand mobile-brand">stay<span>hub</span></Link>
          <p className="eyebrow orange">WELCOME</p>
          <h2>{title}</h2>
          <p className="auth-description">{description}</p>
          {children}
          <p className="auth-footer">
            {footerText} <Link to={footerLink}>{footerLinkText}</Link>
          </p>
        </div>
      </section>
    </main>
  )
}

