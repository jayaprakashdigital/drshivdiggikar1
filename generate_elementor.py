#!/usr/bin/env python3
"""Generate Elementor-compatible JSON template from the design HTML."""
import json, random, re

def uid():
    return format(random.randint(0x1000000, 0xFFFFFFF), '07x')

# ── CSS (complete design system) ──────────────────────────────────────────────
CSS = """
:root {
  --blue-950:#04152d;--blue-900:#0a2540;--blue-800:#0d3660;
  --blue-700:#1251a3;--blue-600:#1a6ed8;--blue-500:#2589ff;
  --blue-400:#5aaeff;--blue-300:#93cbff;--blue-100:#deeeff;--blue-50:#f0f8ff;
  --slate-900:#0f172a;--slate-800:#1e293b;--slate-700:#334155;
  --slate-600:#475569;--slate-500:#64748b;--slate-400:#94a3b8;
  --slate-200:#e2e8f0;--slate-100:#f1f5f9;--slate-50:#f8fafc;
  --white:#ffffff;
  --text-primary:var(--slate-900);--text-secondary:var(--slate-600);
  --text-muted:var(--slate-400);--border:var(--slate-200);--border-blue:#c0d9f5;
  --grad-primary:linear-gradient(135deg,#0a2540 0%,#1251a3 55%,#2589ff 100%);
  --grad-blue:linear-gradient(135deg,#1251a3 0%,#2589ff 100%);
  --grad-subtle:linear-gradient(180deg,#f0f8ff 0%,#ffffff 100%);
  --shadow-xs:0 1px 3px rgba(10,37,64,.08);
  --shadow-sm:0 2px 8px rgba(10,37,64,.10),0 1px 3px rgba(10,37,64,.06);
  --shadow-md:0 4px 20px rgba(10,37,64,.12),0 2px 6px rgba(10,37,64,.06);
  --shadow-lg:0 12px 40px rgba(10,37,64,.16),0 4px 12px rgba(10,37,64,.08);
  --r-sm:8px;--r-md:12px;--r-lg:20px;--r-xl:28px;--r-full:999px;
  --sp-1:8px;--sp-2:16px;--sp-3:24px;--sp-4:32px;
  --sp-5:40px;--sp-6:48px;--sp-7:64px;--sp-8:80px;--sp-9:96px;--sp-10:120px;
  --transition:all 0.22s cubic-bezier(0.4,0,0.2,1);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
.shiv-page img{max-width:100%;height:auto;display:block;}
.shiv-page a{text-decoration:none;color:inherit;}
.shiv-page button{font-family:inherit;}
.shiv-wrap{max-width:1160px;margin:0 auto;padding:0 24px;}
.shiv-page h1,.shiv-page h2,.shiv-page h3{
  font-family:'Bricolage Grotesque','Inter',sans-serif;
  letter-spacing:-0.02em;line-height:1.1;
}
.shiv-page h1{font-size:clamp(36px,5vw,60px);font-weight:800;}
.shiv-page h2{font-size:clamp(26px,3.5vw,40px);font-weight:700;color:var(--slate-900);}
.shiv-page h3{font-size:clamp(16px,2vw,20px);font-weight:700;color:var(--slate-900);}
.shiv-page p{line-height:1.75;color:var(--text-secondary);}
.shiv-page p:not(:last-child){margin-bottom:14px;}

/* section-tag */
.sec-tag{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:700;
  letter-spacing:2px;text-transform:uppercase;color:var(--blue-600);background:var(--blue-50);
  border:1px solid var(--border-blue);padding:5px 14px;border-radius:var(--r-full);margin-bottom:16px;}
.sec-tag-w{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:700;
  letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.9);
  background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);
  padding:5px 14px;border-radius:var(--r-full);margin-bottom:16px;}
.sec-sub{font-size:17px;color:var(--text-secondary);max-width:640px;line-height:1.7;margin-bottom:40px;}

/* buttons */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;
  padding:14px 28px;border-radius:var(--r-full);font-size:15px;font-weight:600;
  font-family:'Inter',sans-serif;cursor:pointer;border:none;
  transition:var(--transition);white-space:nowrap;text-decoration:none;letter-spacing:-.01em;}
.btn-primary{background:var(--grad-blue);color:var(--white);box-shadow:0 2px 12px rgba(37,137,255,.35);}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 6px 24px rgba(37,137,255,.45);}
.btn-white{background:var(--white);color:var(--blue-700);box-shadow:var(--shadow-sm);}
.btn-white:hover{transform:translateY(-2px);box-shadow:var(--shadow-md);}
.btn-ghost{background:rgba(255,255,255,.12);color:var(--white);
  border:1.5px solid rgba(255,255,255,.35);backdrop-filter:blur(8px);}
.btn-ghost:hover{background:rgba(255,255,255,.2);border-color:rgba(255,255,255,.6);}
.btn-outline-blue{background:transparent;color:var(--blue-600);border:1.5px solid var(--border-blue);}
.btn-outline-blue:hover{background:var(--blue-50);border-color:var(--blue-600);}

/* mobile sticky */
.mobile-sticky-cta{display:none;position:fixed;bottom:0;left:0;right:0;z-index:900;
  padding:12px 16px;background:rgba(255,255,255,.95);backdrop-filter:blur(12px);
  border-top:1px solid var(--border);gap:10px;box-shadow:0 -4px 20px rgba(10,37,64,.12);}
.mobile-sticky-cta .btn{flex:1;padding:13px 12px;font-size:14px;}

/* ── HERO ── */
.shiv-hero{position:relative;display:flex;align-items:center;overflow:hidden;background:var(--blue-900);}
.hero-bg{position:absolute;inset:0;z-index:0;}
.hero-bg img{width:100%;height:100%;object-fit:cover;object-position:center 20%;opacity:.35;}
.hero-overlay{position:absolute;inset:0;z-index:1;
  background:radial-gradient(ellipse 80% 60% at 20% 50%,rgba(18,81,163,.85) 0%,transparent 70%),
             radial-gradient(ellipse 60% 80% at 80% 20%,rgba(37,137,255,.3) 0%,transparent 60%),
             linear-gradient(160deg,rgba(4,21,45,.95) 0%,rgba(10,37,64,.75) 100%);}
.hero-orb{position:absolute;border-radius:50%;pointer-events:none;z-index:1;}
.hero-orb-1{width:400px;height:400px;top:-100px;right:-80px;
  background:radial-gradient(circle,rgba(37,137,255,.15) 0%,transparent 70%);}
.hero-orb-2{width:300px;height:300px;bottom:-60px;left:10%;
  background:radial-gradient(circle,rgba(18,81,163,.2) 0%,transparent 70%);}
.hero-inner{position:relative;z-index:2;width:100%;padding:96px 0 72px;}
.hero-layout{display:grid;grid-template-columns:1fr 380px;gap:64px;align-items:center;}
.hero-badge{display:inline-flex;align-items:center;gap:8px;
  background:rgba(37,137,255,.15);border:1px solid rgba(90,174,255,.35);
  border-radius:var(--r-full);padding:6px 16px 6px 8px;
  font-size:12px;font-weight:600;color:var(--blue-300);letter-spacing:.5px;margin-bottom:24px;}
.hero-badge-dot{width:8px;height:8px;background:#22c55e;border-radius:50%;
  flex-shrink:0;box-shadow:0 0 0 3px rgba(34,197,94,.2);}
.shiv-hero h1{color:var(--white);margin-bottom:20px;}
.shiv-hero h1 em{font-style:normal;color:var(--blue-400);}
.hero-desc{color:rgba(255,255,255,.72);font-size:17px;line-height:1.7;margin-bottom:36px;max-width:560px;}
.hero-ctas{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:48px;}
.hero-trust{display:flex;align-items:center;gap:16px;flex-wrap:wrap;}
.hero-trust-item{display:flex;align-items:center;gap:6px;font-size:13px;
  color:rgba(255,255,255,.65);font-weight:500;}
.hero-trust-div{width:1px;height:16px;background:rgba(255,255,255,.2);}
.hero-card{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);
  border-radius:var(--r-xl);padding:28px;backdrop-filter:blur(16px);}
.hero-card-hdr{display:flex;align-items:center;gap:14px;
  padding-bottom:20px;border-bottom:1px solid rgba(255,255,255,.1);margin-bottom:20px;}
.hero-avatar{width:56px;height:56px;background:var(--grad-blue);color:var(--white);
  border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-size:22px;flex-shrink:0;box-shadow:0 4px 16px rgba(37,137,255,.4);}
.hero-card-name{font-size:16px;font-weight:700;color:var(--white);line-height:1.3;}
.hero-card-ttl{font-size:12px;color:rgba(255,255,255,.55);margin-top:3px;}
.cred-list{display:flex;flex-direction:column;gap:10px;}
.cred-item{display:flex;align-items:flex-start;gap:10px;padding:10px 12px;
  background:rgba(255,255,255,.05);border-radius:var(--r-md);
  border:1px solid rgba(255,255,255,.08);transition:background .2s;}
.cred-item:hover{background:rgba(255,255,255,.09);}
.cred-icon{display:flex;align-items:center;justify-content:center;
  flex-shrink:0;color:var(--blue-400);width:20px;height:20px;}
.cred-text{font-size:13px;color:rgba(255,255,255,.82);font-weight:500;line-height:1.4;}
.cred-sub{font-size:11px;color:rgba(255,255,255,.4);margin-top:2px;display:block;}

/* ── ABOUT ── */
.shiv-about{padding:120px 0;background:var(--white);}
.about-layout{display:grid;grid-template-columns:1fr 440px;gap:72px;
  align-items:start;margin-top:40px;}
.about-text p{font-size:16px;line-height:1.85;color:var(--text-secondary);}
.about-text p strong{color:var(--slate-800);}
.about-text p:not(:last-child){margin-bottom:18px;}
.about-hi{display:flex;flex-direction:column;gap:12px;margin-top:40px;}
.hi-item{display:flex;align-items:center;gap:12px;padding:14px 16px;
  background:var(--blue-50);border:1px solid var(--border-blue);
  border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--blue-800);
  transition:var(--transition);}
.hi-item:hover{background:var(--blue-100);transform:translateX(4px);}
.hi-icon{display:flex;align-items:center;justify-content:center;
  flex-shrink:0;color:var(--blue-600);width:20px;height:20px;}
.about-sidebar{display:flex;flex-direction:column;gap:16px;position:sticky;top:32px;}
.profile-card{background:var(--grad-primary);border-radius:var(--r-xl);
  padding:28px;color:var(--white);position:relative;overflow:hidden;}
.profile-card::before{content:'';position:absolute;top:-40px;right:-40px;
  width:180px;height:180px;border-radius:50%;background:rgba(255,255,255,.06);pointer-events:none;}
.profile-card::after{content:'';position:absolute;bottom:-30px;left:-20px;
  width:140px;height:140px;border-radius:50%;background:rgba(255,255,255,.04);pointer-events:none;}
.pname{font-family:'Bricolage Grotesque',sans-serif;font-size:20px;font-weight:700;
  color:var(--white);margin-bottom:4px;position:relative;}
.ptitle{font-size:13px;color:rgba(255,255,255,.65);margin-bottom:20px;position:relative;}
.pstats{display:grid;grid-template-columns:1fr 1fr;gap:10px;position:relative;}
.pstat{background:rgba(255,255,255,.1);border-radius:var(--r-md);
  padding:14px 12px;text-align:center;}
.pstat-n{font-family:'Bricolage Grotesque',sans-serif;font-size:24px;font-weight:800;
  color:var(--white);line-height:1;}
.pstat-l{font-size:11px;color:rgba(255,255,255,.6);margin-top:3px;}
.int-links{margin-top:24px;padding:18px 22px;background:var(--white);
  border-radius:var(--r-md);border:1px solid var(--border-blue);border-left:4px solid var(--blue-600);}
.int-links p{font-size:14px;color:var(--text-secondary);margin:0 0 6px;}
.int-links a{color:var(--blue-600);font-weight:600;}
.int-links a:hover{text-decoration:underline;}
.hours-card{background:var(--slate-50);border:1px solid var(--border);
  border-radius:var(--r-lg);padding:20px;}
.hours-card h4{font-size:13px;font-weight:700;text-transform:uppercase;
  letter-spacing:1px;color:var(--text-muted);margin-bottom:12px;}
.hours-row{display:flex;justify-content:space-between;align-items:center;
  font-size:14px;padding:8px 0;border-bottom:1px solid var(--border);color:var(--slate-700);}
.hours-row:last-child{border-bottom:none;}
.hours-row strong{color:var(--slate-900);font-weight:600;}
.hours-open{font-size:11px;font-weight:700;color:#16a34a;background:#dcfce7;
  padding:2px 8px;border-radius:var(--r-full);}

/* ── WHY ── */
.shiv-why{padding:120px 0;background:var(--grad-primary);position:relative;overflow:hidden;}
.shiv-why::before{content:'';position:absolute;top:-120px;right:-80px;width:500px;height:500px;
  border-radius:50%;background:radial-gradient(circle,rgba(37,137,255,.12) 0%,transparent 70%);pointer-events:none;}
.shiv-why::after{content:'';position:absolute;bottom:-100px;left:-60px;width:400px;height:400px;
  border-radius:50%;background:radial-gradient(circle,rgba(18,81,163,.15) 0%,transparent 70%);pointer-events:none;}
.shiv-why h2{color:var(--white);}
.shiv-why .sec-sub{color:rgba(255,255,255,.7);}
.why-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:40px;position:relative;}
.why-card{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);
  border-radius:var(--r-lg);padding:28px;backdrop-filter:blur(12px);
  transition:var(--transition);position:relative;overflow:hidden;}
.why-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,rgba(90,174,255,.5),transparent);
  opacity:0;transition:opacity .3s;}
.why-card:hover{background:rgba(255,255,255,.1);transform:translateY(-6px);
  box-shadow:0 16px 40px rgba(0,0,0,.25);}
.why-card:hover::before{opacity:1;}
.why-num{font-family:'Bricolage Grotesque',sans-serif;font-size:13px;font-weight:700;
  color:var(--blue-300);letter-spacing:1.5px;margin-bottom:14px;display:block;}
.why-icon{width:48px;height:48px;background:rgba(37,137,255,.15);
  border:1px solid rgba(90,174,255,.25);border-radius:var(--r-md);
  display:flex;align-items:center;justify-content:center;margin-bottom:18px;color:var(--blue-300);}
.why-card h3{color:var(--white);font-size:17px;margin-bottom:10px;}
.why-card p{font-size:14px;color:rgba(255,255,255,.68);line-height:1.7;margin:0;}

/* ── SERVICES ── */
.shiv-svc{padding:120px 0;background:var(--grad-subtle);}
.svc-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:40px;}
.svc-card{background:var(--white);border:1px solid var(--border);
  border-radius:var(--r-lg);padding:24px;transition:var(--transition);}
.svc-card:hover{transform:translateY(-4px);box-shadow:var(--shadow-md);border-color:var(--border-blue);}
.svc-icon{width:44px;height:44px;border-radius:var(--r-md);background:var(--blue-50);
  border:1px solid var(--border-blue);color:var(--blue-600);
  display:flex;align-items:center;justify-content:center;margin-bottom:16px;}
.svc-card h3{font-size:16px;color:var(--slate-900);margin-bottom:8px;}
.svc-card p{font-size:13.5px;line-height:1.65;color:var(--text-secondary);margin:0;}

/* ── LOCATION ── */
.shiv-loc{padding:120px 0;background:var(--white);}
.loc-layout{margin-top:40px;display:grid;grid-template-columns:1fr 340px;gap:28px;align-items:start;}
.loc-main{background:var(--white);border:1px solid var(--border);
  border-radius:var(--r-xl);overflow:hidden;box-shadow:var(--shadow-md);}
.loc-hdr{padding:28px 28px 20px;
  background:linear-gradient(135deg,var(--blue-50) 0%,var(--white) 100%);
  border-bottom:1px solid var(--border);}
.loc-badge{display:inline-flex;align-items:center;gap:6px;font-size:10px;font-weight:700;
  letter-spacing:1.5px;text-transform:uppercase;background:var(--blue-600);
  color:var(--white);padding:4px 12px;border-radius:var(--r-full);margin-bottom:12px;}
.loc-title{font-size:18px;font-weight:700;color:var(--slate-900);}
.loc-body{padding:24px 28px;}
.loc-details{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:24px;}
.loc-lbl{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;
  color:var(--text-muted);margin-bottom:5px;}
.loc-val{font-size:14.5px;color:var(--slate-700);line-height:1.5;margin:0;}
.areas-block{padding:16px 18px;background:var(--slate-50);border-radius:var(--r-md);
  font-size:13px;color:var(--text-secondary);line-height:1.7;margin-bottom:20px;
  border:1px solid var(--border);}
.areas-block strong{color:var(--slate-800);display:block;margin-bottom:6px;
  font-size:12px;text-transform:uppercase;letter-spacing:1px;}
.area-tag{display:inline-block;padding:4px 10px;background:var(--white);
  border:1px solid var(--border-blue);border-radius:var(--r-full);
  font-size:12px;color:var(--blue-700);font-weight:600;margin:4px 4px 0 0;}
.loc-cta{display:inline-flex;align-items:center;gap:8px;padding:13px 28px;
  background:var(--grad-blue);color:var(--white);border-radius:var(--r-full);
  font-size:15px;font-weight:600;transition:var(--transition);
  box-shadow:0 2px 12px rgba(37,137,255,.35);}
.loc-cta:hover{transform:translateY(-2px);box-shadow:0 6px 24px rgba(37,137,255,.45);}
.contact-sidebar{display:flex;flex-direction:column;gap:16px;}
.contact-card{background:var(--grad-primary);border-radius:var(--r-xl);
  padding:24px;color:var(--white);position:relative;overflow:hidden;}
.contact-card::before{content:'';position:absolute;top:-30px;right:-30px;
  width:150px;height:150px;border-radius:50%;background:rgba(255,255,255,.05);}
.contact-card h3{font-size:16px;font-weight:700;color:var(--white);
  margin-bottom:16px;position:relative;}
.contact-row{display:flex;align-items:center;gap:10px;padding:12px 14px;
  background:rgba(255,255,255,.08);border-radius:var(--r-md);
  font-size:14.5px;font-weight:600;color:rgba(255,255,255,.9);
  margin-bottom:8px;text-decoration:none;transition:background .2s;position:relative;}
.contact-row:hover{background:rgba(255,255,255,.14);}
.same-day{font-size:12.5px;color:rgba(255,255,255,.65);font-style:italic;margin:4px 0 0;position:relative;}
.sec-clinic{background:var(--white);border:1px dashed var(--border-blue);
  border-radius:var(--r-lg);padding:18px 20px;}
.sec-clinic h4{font-size:11px;font-weight:700;text-transform:uppercase;
  letter-spacing:1.5px;color:var(--blue-600);margin-bottom:8px;}
.sec-clinic strong{color:var(--slate-900);display:block;font-size:14.5px;margin-bottom:4px;}
.sec-clinic p{font-size:13px;color:var(--text-secondary);line-height:1.6;margin:0;}

/* ── TESTIMONIALS ── */
.shiv-test{padding:120px 0;background:var(--slate-50);}
.test-hdr{display:flex;align-items:flex-end;justify-content:space-between;
  margin-bottom:40px;flex-wrap:wrap;gap:16px;}
.test-rating{display:flex;align-items:center;gap:8px;}
.stars-lg{color:#f59e0b;font-size:22px;letter-spacing:2px;}
.rating-txt{font-size:14px;color:var(--text-muted);font-weight:500;}
.carousel{position:relative;overflow:hidden;}
.t-card{display:none;animation:slideIn .4s cubic-bezier(.4,0,.2,1);}
.t-card.active{display:block;}
@keyframes slideIn{from{opacity:0;transform:translateX(20px)}to{opacity:1;transform:translateX(0)}}
.tcard-in{background:var(--white);border:1px solid var(--border);border-radius:var(--r-xl);
  padding:40px;max-width:820px;margin:0 auto;box-shadow:var(--shadow-sm);}
.tquote{font-size:64px;line-height:.8;color:var(--blue-100);font-family:Georgia,serif;
  margin-bottom:8px;user-select:none;}
.tstars{color:#f59e0b;font-size:18px;letter-spacing:2px;margin-bottom:14px;}
.theadline{font-family:'Bricolage Grotesque',sans-serif;font-size:20px;font-weight:700;
  color:var(--slate-900);margin-bottom:14px;line-height:1.3;}
.ttext{font-size:16px;line-height:1.8;color:var(--slate-700);margin-bottom:28px;font-style:italic;}
.tauthor{display:flex;align-items:center;gap:14px;}
.tavatar{width:48px;height:48px;border-radius:50%;background:var(--grad-blue);
  color:var(--white);font-size:15px;font-weight:700;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.tname{font-size:15px;font-weight:700;color:var(--slate-900);}
.tloc{font-size:12.5px;color:var(--text-muted);margin-top:2px;}
.carousel-nav{display:flex;align-items:center;justify-content:center;gap:12px;margin-top:24px;}
.c-btn{width:40px;height:40px;border-radius:50%;border:1.5px solid var(--border);
  background:var(--white);color:var(--slate-600);font-size:16px;cursor:pointer;
  transition:var(--transition);display:flex;align-items:center;justify-content:center;
  box-shadow:var(--shadow-xs);}
.c-btn:hover{background:var(--blue-600);color:var(--white);
  border-color:var(--blue-600);box-shadow:0 4px 14px rgba(37,137,255,.3);}
.c-dots{display:flex;gap:6px;}
.c-dot{width:8px;height:8px;border-radius:50%;background:var(--slate-200);
  cursor:pointer;transition:var(--transition);border:none;}
.c-dot.active{background:var(--blue-600);width:24px;border-radius:4px;}

/* ── FAQ ── */
.shiv-faq{padding:120px 0;background:var(--white);}
.faq-layout{display:grid;grid-template-columns:300px 1fr;gap:64px;
  align-items:start;margin-top:40px;}
.faq-sidebar{position:sticky;top:40px;}
.faq-side-card{background:var(--grad-primary);border-radius:var(--r-xl);
  padding:28px;color:var(--white);position:relative;overflow:hidden;}
.faq-side-card::before{content:'';position:absolute;top:-40px;right:-40px;
  width:160px;height:160px;border-radius:50%;background:rgba(255,255,255,.06);}
.faq-side-card h3{color:var(--white);font-size:18px;margin-bottom:10px;position:relative;}
.faq-side-card p{font-size:14px;color:rgba(255,255,255,.7);line-height:1.65;
  margin-bottom:24px;position:relative;}
.faq-side-card .btn{width:100%;justify-content:center;position:relative;}
.faq-list{display:flex;flex-direction:column;gap:4px;}
.faq-item{border:1px solid var(--border);border-radius:var(--r-md);
  overflow:hidden;transition:border-color .2s,box-shadow .2s;}
.faq-item:hover{border-color:var(--border-blue);}
.faq-item.is-open{border-color:var(--blue-600);box-shadow:0 0 0 3px rgba(37,137,255,.08);}
.faq-q{width:100%;display:flex;align-items:center;justify-content:space-between;
  padding:18px 20px;background:var(--white);border:none;cursor:pointer;
  font-size:15px;font-weight:600;color:var(--slate-800);font-family:'Inter',sans-serif;
  text-align:left;gap:16px;transition:background .2s;line-height:1.4;}
.faq-q:hover{background:var(--blue-50);}
.faq-qi{width:28px;height:28px;border-radius:50%;background:var(--slate-100);
  display:flex;align-items:center;justify-content:center;flex-shrink:0;
  transition:var(--transition);color:var(--slate-500);font-size:18px;font-weight:300;line-height:1;}
.faq-item.is-open .faq-qi{background:var(--blue-600);color:var(--white);transform:rotate(45deg);}
.faq-a{max-height:0;overflow:hidden;transition:max-height .38s cubic-bezier(.4,0,.2,1);}
.faq-a.open{max-height:700px;}
.faq-a p{padding:0 20px 20px;font-size:14.5px;line-height:1.75;color:var(--text-secondary);margin:0;}
.faq-a a{color:var(--blue-600);font-weight:600;}

/* ── FINAL CTA ── */
.shiv-cta{padding:120px 0;background:var(--grad-primary);text-align:center;
  position:relative;overflow:hidden;}
.shiv-cta::before{content:'';position:absolute;top:-100px;right:-100px;width:500px;height:500px;
  border-radius:50%;background:radial-gradient(circle,rgba(37,137,255,.12) 0%,transparent 70%);pointer-events:none;}
.shiv-cta::after{content:'';position:absolute;bottom:-80px;left:-80px;width:400px;height:400px;
  border-radius:50%;background:radial-gradient(circle,rgba(18,81,163,.15) 0%,transparent 70%);pointer-events:none;}
.cta-in{position:relative;max-width:760px;margin:0 auto;}
.shiv-cta h2{color:var(--white);margin-bottom:16px;}
.cta-desc{color:rgba(255,255,255,.78);font-size:17px;line-height:1.75;margin-bottom:40px;}
.cta-btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-bottom:48px;}
.cta-trust{display:flex;justify-content:center;flex-wrap:wrap;gap:24px;margin-bottom:24px;}
.cta-trust-item{display:flex;align-items:center;gap:8px;color:rgba(255,255,255,.85);
  font-size:14px;font-weight:500;}
.cta-trust-icon{display:flex;align-items:center;justify-content:center;color:var(--blue-300);flex-shrink:0;}
.cta-areas{font-size:12.5px;color:rgba(255,255,255,.5);}

/* ── SCROLL REVEAL ── */
.reveal{opacity:0;transform:translateY(18px);transition:opacity .5s ease,transform .5s ease;}
.reveal.visible{opacity:1;transform:translateY(0);}

/* ── RESPONSIVE ── */
@media(max-width:1024px){
  .hero-layout{grid-template-columns:1fr;max-width:640px;}
  .hero-card{display:none;}
  .about-layout{grid-template-columns:1fr;gap:48px;}
  .about-sidebar{position:static;}
  .why-grid{grid-template-columns:repeat(2,1fr);}
  .svc-grid{grid-template-columns:repeat(2,1fr);}
  .loc-layout{grid-template-columns:1fr;}
  .faq-layout{grid-template-columns:1fr;}
  .faq-sidebar{position:static;}
}
@media(max-width:767px){
  .shiv-hero .hero-inner,.shiv-about,.shiv-why,.shiv-svc,.shiv-loc,.shiv-test,.shiv-faq,.shiv-cta
    {padding-top:72px;padding-bottom:72px;}
  .hero-inner{padding:80px 0 100px!important;}
  .shiv-hero h1{font-size:32px;}
  .hero-desc{font-size:15px;}
  .hero-ctas{flex-direction:column;}
  .hero-ctas .btn{width:100%;justify-content:center;}
  .hero-trust{gap:10px;}
  .hero-trust-div{display:none;}
  .why-grid{grid-template-columns:1fr;gap:12px;}
  .svc-grid{grid-template-columns:1fr;}
  .why-card,.svc-card{padding:22px;}
  .loc-details{grid-template-columns:1fr;gap:14px;}
  .loc-hdr{padding:20px 20px 16px;}
  .loc-body{padding:18px 20px;}
  .tcard-in{padding:24px 20px;}
  .ttext{font-size:15px;}
  .tquote{font-size:48px;}
  .faq-q{padding:15px 16px;font-size:14px;}
  .faq-a p{padding:0 16px 18px;font-size:14px;}
  .cta-btns{flex-direction:column;align-items:center;}
  .cta-btns .btn{width:100%;max-width:340px;}
  .cta-trust{gap:14px;}
  .mobile-sticky-cta{display:flex;}
  .about-hi{gap:8px;}
  .pstats{gap:8px;}
  .test-hdr{flex-direction:column;align-items:flex-start;}
}
@media(max-width:480px){
  .shiv-hero h1{font-size:28px;}
  .shiv-page h2{font-size:24px;}
}
"""

# ── SVG ICONS ─────────────────────────────────────────────────────────────────
ICON_CAL = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
ICON_PHONE = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.27h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 9a16 16 0 0 0 6 6l1.09-1.09a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
ICON_CHECK = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>'
ICON_PIN = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
ICON_CLOCK = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
ICON_MEDAL = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89L17 22l-5-3-5 3 1.523-9.11"/></svg>'
ICON_HOME = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>'
ICON_BOOK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>'
ICON_USER = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'

# ── SECTION HTML BLOCKS ───────────────────────────────────────────────────────

HERO_HTML = f"""
<div class="shiv-page">
<section class="shiv-hero">
  <div class="hero-bg">
    <img src="https://images.pexels.com/photos/5452201/pexels-photo-5452201.jpeg?auto=compress&cs=tinysrgb&w=1600" alt="Dr. Shivashankar Diggikar - Top Pediatrician Whitefield" loading="eager"/>
  </div>
  <div class="hero-overlay"></div>
  <div class="hero-orb hero-orb-1"></div>
  <div class="hero-orb hero-orb-2"></div>
  <div class="hero-inner">
    <div class="shiv-wrap">
      <div class="hero-layout">
        <div>
          <div class="hero-badge"><span class="hero-badge-dot"></span>Now consulting &middot; Medicover Whitefield Main Road &middot; Near ITPL</div>
          <h1>Top Pediatrician in Whitefield, Bangalore<br><em>&mdash; Expert Child Care Near ITPL</em></h1>
          <p class="hero-desc">UK &amp; Ireland Certified Pediatrician serving Whitefield, Kadugodi, Varthur, Hoodi, Brookefield &amp; ITPL. Dr. Shivashankar Diggikar &mdash; FRCPCH (UK) &middot; FRCPI (Ireland) &middot; BMJ Paediatrics Editor &middot; 15+ Years Experience.</p>
          <div class="hero-ctas">
            <a href="https://www.medicoverhospitals.in/doctors/dr-shivashankar-diggikar" target="_blank" rel="noopener" class="btn btn-primary">{ICON_CAL} Book Appointment</a>
            <a href="tel:+919133555335" class="btn btn-ghost">{ICON_PHONE.replace('17','17')} +91-9133555335</a>
          </div>
          <div class="hero-trust">
            <span class="hero-trust-item">{ICON_CHECK} FRCPCH (UK) Certified</span>
            <span class="hero-trust-div"></span>
            <span class="hero-trust-item">{ICON_CHECK} Director, Medicover Whitefield</span>
            <span class="hero-trust-div"></span>
            <span class="hero-trust-item">{ICON_CHECK} 24/7 Pediatric Emergency</span>
          </div>
        </div>
        <div class="hero-card">
          <div class="hero-card-hdr">
            <div class="hero-avatar">{ICON_USER}</div>
            <div>
              <div class="hero-card-name">Dr. Shivashankar Diggikar</div>
              <div class="hero-card-ttl">Pediatrician &amp; Neonatologist &middot; Whitefield</div>
            </div>
          </div>
          <div class="cred-list">
            <div class="cred-item"><span class="cred-icon">{ICON_MEDAL}</span><div class="cred-text">FRCPCH<span class="cred-sub">Royal College of Paediatrics &amp; Child Health, UK</span></div></div>
            <div class="cred-item"><span class="cred-icon">{ICON_MEDAL}</span><div class="cred-text">FRCPI<span class="cred-sub">Royal College of Physicians, Ireland</span></div></div>
            <div class="cred-item"><span class="cred-icon">{ICON_HOME}</span><div class="cred-text">Director, Medicover Whitefield<span class="cred-sub">Neonatal-Perinatal Services &amp; Academics</span></div></div>
            <div class="cred-item"><span class="cred-icon">{ICON_PIN}</span><div class="cred-text">London-Trained Neonatologist<span class="cred-sub">Homerton University Hospital, London</span></div></div>
            <div class="cred-item"><span class="cred-icon">{ICON_BOOK}</span><div class="cred-text">Associate Editor<span class="cred-sub">BMJ Paediatrics Open &middot; 30+ Publications</span></div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
</div>
"""

ABOUT_HTML = """
<div class="shiv-page">
<section class="shiv-about">
  <div class="shiv-wrap">
    <div class="sec-tag">Your Neighborhood Pediatrician</div>
    <h2>World-Class Pediatric Care, Right Here in Whitefield</h2>
    <div class="about-layout">
      <div class="about-text">
        <p>Finding a trusted <strong>pediatrician in Whitefield</strong> who combines international training with genuine accessibility for families in your neighborhood is no longer a challenge. Dr. Shivashankar Diggikar brings UK and Ireland-certified pediatric expertise right to your doorstep at <strong>Medicover Women &amp; Children Hospital, Whitefield Main Road</strong> &mdash; just 5 minutes from Forum Neighbourhood Mall and 10 minutes from ITPL.</p>
        <p>Parents in Whitefield, ITPL, Kadugodi, Varthur, Hoodi, Brookefield, Marathahalli, Channasandra, Nallurhalli, and Doddanekkundi no longer need to travel to distant hospitals across Bangalore for world-class pediatric care. Dr. Diggikar is a <strong>top pediatrician in Whitefield</strong> with credentials rarely found in neighborhood clinics: <strong>FRCPCH</strong> (Fellow of the Royal College of Paediatrics and Child Health, UK) and <strong>FRCPI</strong> (Fellow of the Royal College of Physicians of Ireland) &mdash; dual international certifications that ensure your child receives care aligned with UK and European pediatric standards.</p>
        <p>As <strong>Director of Neonatal-Perinatal Services</strong> and Head of Academics at Medicover Whitefield, Dr. Diggikar oversees the entire pediatric department &mdash; from NICU care for premature babies to routine vaccinations, growth monitoring, and management of childhood illnesses.</p>
        <p>His London training at <strong>Homerton University Hospital</strong>, 30+ research publications in international pediatric journals, and role as Associate Editor at <strong>BMJ Paediatrics Open</strong> mean you&rsquo;re getting evidence-based care backed by the latest global research.</p>
        <div class="about-hi">
          <div class="hi-item"><span class="hi-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></span>5 min from Forum Mall &middot; 10 min from ITPL &middot; Connected by Whitefield Metro</div>
          <div class="hi-item"><span class="hi-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89L17 22l-5-3-5 3 1.523-9.11"/></svg></span>Dual UK + Ireland fellowships &mdash; rare among Bangalore pediatricians</div>
          <div class="hi-item"><span class="hi-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></span>Director of Neonatal-Perinatal Services, Medicover Whitefield</div>
          <div class="hi-item"><span class="hi-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></span>Mon&ndash;Sat, 9:30 AM &ndash; 2:30 PM &middot; 24/7 Pediatric Emergency</div>
        </div>
        <div class="int-links">
          <p><strong>Related Reading</strong></p>
          <p><a href="/nicu-specialist-bangalore">&rarr; Specialized NICU care for premature babies</a><br><a href="/newborn-care">&rarr; Comprehensive newborn care services for new parents in Whitefield</a></p>
        </div>
      </div>
      <div class="about-sidebar">
        <div class="profile-card">
          <div class="pname">Dr. Shivashankar Diggikar</div>
          <div class="ptitle">FRCPCH &middot; FRCPI &middot; MRCPCH &middot; MD</div>
          <div class="pstats">
            <div class="pstat"><div class="pstat-n">15+</div><div class="pstat-l">Years Exp.</div></div>
            <div class="pstat"><div class="pstat-n">30+</div><div class="pstat-l">Publications</div></div>
            <div class="pstat"><div class="pstat-n">2</div><div class="pstat-l">Fellowships</div></div>
            <div class="pstat"><div class="pstat-n">24/7</div><div class="pstat-l">Emergency</div></div>
          </div>
        </div>
        <div class="hours-card">
          <h4>Clinic Hours &middot; Whitefield</h4>
          <div class="hours-row"><strong>Mon &ndash; Sat</strong><span>9:30 AM &ndash; 2:30 PM</span></div>
          <div class="hours-row"><strong>Sunday</strong><span>Closed (Emergency 24/7)</span></div>
          <div class="hours-row"><strong>Status</strong><span><span class="hours-open">Open today</span></span></div>
        </div>
      </div>
    </div>
  </div>
</section>
</div>
"""

WHY_HTML = """
<div class="shiv-page">
<section class="shiv-why">
  <div class="shiv-wrap">
    <div class="sec-tag-w">Why Whitefield Families Choose Dr. Diggikar</div>
    <h2>Six reasons Whitefield families trust their child&rsquo;s care to Dr. Diggikar.</h2>
    <p class="sec-sub">International training, deep neonatology specialization, and proximity to your neighborhood &mdash; under one roof.</p>
    <div class="why-grid">
      <div class="why-card">
        <span class="why-num">01</span>
        <div class="why-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 1 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div>
        <h3>Conveniently Located in Whitefield</h3>
        <p>Medicover Whitefield Main Road &mdash; 5 min from Forum Mall, 10 min from ITPL. Connected by Whitefield Metro (Purple Line). Ample free parking.</p>
      </div>
      <div class="why-card">
        <span class="why-num">02</span>
        <div class="why-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89L17 22l-5-3-5 3 1.523-9.11"/></svg></div>
        <h3>FRCPCH (UK) &amp; FRCPI (Ireland)</h3>
        <p>Dual international fellowships from the UK and Ireland &mdash; credentials very few neighborhood pediatricians in Bangalore hold. Care aligned with European standards.</p>
      </div>
      <div class="why-card">
        <span class="why-num">03</span>
        <div class="why-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-4-7-11a7 7 0 0 1 14 0c0 7-7 11-7 11z"/><path d="M12 11v4"/><path d="M10 13h4"/></svg></div>
        <h3>London-Trained Neonatologist</h3>
        <p>Fellowship at Homerton University Hospital, London. Complex newborn cases, premature babies, and NICU admissions &mdash; handled right here in Whitefield.</p>
      </div>
      <div class="why-card">
        <span class="why-num">04</span>
        <div class="why-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></div>
        <h3>Director, Medicover Whitefield</h3>
        <p>Director of Neonatal-Perinatal Services &amp; Head of Academics. Access to Level III NICU, 24/7 emergency, and a full pediatric support team &mdash; all in Whitefield.</p>
      </div>
      <div class="why-card">
        <span class="why-num">05</span>
        <div class="why-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg></div>
        <h3>30+ Publications &amp; BMJ Editor</h3>
        <p>Associate Editor at BMJ Paediatrics Open with 30+ international publications. Evidence-based, research-backed treatment protocols &mdash; not outdated practice.</p>
      </div>
      <div class="why-card">
        <span class="why-num">06</span>
        <div class="why-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></div>
        <h3>15+ Years &middot; Trusted by Thousands</h3>
        <p>From newborn emergencies to chronic conditions &mdash; Dr. Diggikar has seen and successfully treated nearly every pediatric concern Whitefield parents worry about.</p>
      </div>
    </div>
  </div>
</section>
</div>
"""

SERVICES_HTML = """
<div class="shiv-page">
<section class="shiv-svc">
  <div class="shiv-wrap">
    <div class="sec-tag">Pediatric Services</div>
    <h2>Comprehensive Child Healthcare for Whitefield Families</h2>
    <p class="sec-sub">From the first 28 days of life through adolescence &mdash; one trusted doctor, end to end.</p>
    <div class="svc-grid">
      <div class="svc-card">
        <div class="svc-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg></div>
        <h3>Newborn Care (0&ndash;28 Days)</h3>
        <p>Complete health checks, jaundice phototherapy, feeding support, cord care, newborn screening, and safe discharge planning.</p>
      </div>
      <div class="svc-card">
        <div class="svc-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M19 9V6a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v3"/><rect x="3" y="9" width="18" height="12" rx="2"/><path d="M8 13h8"/></svg></div>
        <h3>Vaccinations &amp; Immunizations</h3>
        <p>Full IAP 2025 schedule &mdash; BCG, Hep B, DPT, MMR, Varicella, Rotavirus, Pneumococcal, HPV. Catch-up schedules included.</p>
      </div>
      <div class="svc-card">
        <div class="svc-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M7 14l3-3 3 3 5-5"/></svg></div>
        <h3>Growth &amp; Development</h3>
        <p>WHO-chart tracking for weight, height, head circumference. Milestone assessments and early identification of delays.</p>
      </div>
      <div class="svc-card">
        <div class="svc-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4"/><path d="M9 7h6a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3H9a3 3 0 0 1-3-3v-8a3 3 0 0 1 3-3z"/><path d="M9 13h6"/></svg></div>
        <h3>Sick Child Consultations</h3>
        <p>Fever, infections, ear/throat issues, diarrhea, cough &amp; cold, UTIs, rashes. Walk-ins accepted during clinic hours.</p>
      </div>
      <div class="svc-card">
        <div class="svc-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 12c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M3 12h3M18 12h3M12 3v3M12 18v3"/><circle cx="12" cy="12" r="2"/></svg></div>
        <h3>Asthma &amp; Allergy Care</h3>
        <p>Personalized action plans for asthma, allergic rhinitis, eczema, and food allergies &mdash; common in Whitefield/ITPL areas.</p>
      </div>
      <div class="svc-card">
        <div class="svc-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2c1.7 4 3 6 6 8-3 2-4.3 4-6 8-1.7-4-3-6-6-8 3-2 4.3-4 6-8z"/></svg></div>
        <h3>Nutrition &amp; Feeding</h3>
        <p>Breastfeeding support, formula advice, solids transition, picky eaters, nutrient deficiencies, and obesity counseling.</p>
      </div>
      <div class="svc-card">
        <div class="svc-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l3-9 4 18 3-9h4"/></svg></div>
        <h3>Chronic Disease Management</h3>
        <p>Type 1 diabetes, thyroid disorders, epilepsy, ADHD, autism &mdash; long-term monitoring with specialist coordination.</p>
      </div>
      <div class="svc-card">
        <div class="svc-icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v10M7 12h10"/></svg></div>
        <h3>24/7 Pediatric Emergency</h3>
        <p>High fever, dehydration, breathing distress, seizures, head injuries. Round-the-clock at Medicover Whitefield.</p>
      </div>
    </div>
  </div>
</section>
</div>
"""

LOCATION_HTML = """
<div class="shiv-page">
<section class="shiv-loc">
  <div class="shiv-wrap">
    <div class="sec-tag">Convenient Whitefield Location</div>
    <h2>Easy to Reach from Anywhere in Whitefield</h2>
    <div class="loc-layout">
      <div class="loc-main">
        <div class="loc-hdr">
          <div class="loc-badge">Primary Clinic</div>
          <div class="loc-title">Medicover Women &amp; Children Hospital, Whitefield</div>
        </div>
        <div class="loc-body">
          <div class="loc-details">
            <div><div class="loc-lbl">Address</div><p class="loc-val">Whitefield Main Road, Whitefield, Bangalore &mdash; 560066</p></div>
            <div><div class="loc-lbl">Consultation Hours</div><p class="loc-val">Monday&ndash;Saturday<br>9:30 AM &ndash; 2:30 PM</p></div>
            <div><div class="loc-lbl">Phone</div><p class="loc-val"><a href="tel:+919133555335" style="color:#1a6ed8;">+91-9133555335</a><br>24/7 Pediatric Emergency</p></div>
            <div><div class="loc-lbl">Insurance</div><p class="loc-val">All major insurance providers accepted at Medicover Whitefield</p></div>
            <div><div class="loc-lbl">By Car</div><p class="loc-val">5 min from Forum Mall &middot; 10 min from ITPL &middot; 12 min from Kadugodi &middot; 15 min from Varthur / Hoodi</p></div>
            <div><div class="loc-lbl">By Metro</div><p class="loc-val">Whitefield Metro (Purple Line) &mdash; 8 min by auto &middot; ITPL Metro &mdash; 12 min by auto</p></div>
          </div>
          <div class="areas-block">
            <strong>Serving families across</strong>
            <span class="area-tag">Whitefield</span><span class="area-tag">ITPL</span><span class="area-tag">Kadugodi</span><span class="area-tag">Varthur</span><span class="area-tag">Hoodi</span><span class="area-tag">Brookefield</span><span class="area-tag">Marathahalli</span><span class="area-tag">Channasandra</span><span class="area-tag">Nallurhalli</span><span class="area-tag">Doddanekkundi</span><span class="area-tag">Mahadevapura</span><span class="area-tag">Hopefarm</span><span class="area-tag">Ramagondanahalli</span>
          </div>
          <a href="https://www.medicoverhospitals.in/doctors/dr-shivashankar-diggikar" target="_blank" rel="noopener" class="loc-cta">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            Book at Medicover Whitefield
          </a>
        </div>
      </div>
      <div class="contact-sidebar">
        <div class="contact-card">
          <h3>Quick Contact</h3>
          <a href="tel:+919133555335" class="contact-row">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.27h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 9a16 16 0 0 0 6 6l1.09-1.09a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            +91-9133555335
          </a>
          <a href="https://www.medicoverhospitals.in/doctors/dr-shivashankar-diggikar" target="_blank" rel="noopener" class="contact-row">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            Book Online
          </a>
          <p class="same-day">Walk-ins accepted for sick child visits during clinic hours.</p>
        </div>
        <div class="sec-clinic">
          <h4>Secondary Evening Clinic</h4>
          <strong>Oyster Mother &amp; Child Hospital, Banaswadi</strong>
          <p>Mon&ndash;Sat, 5:30 PM &ndash; 7:00 PM &middot; Convenient when traveling from Whitefield toward Old Bangalore.</p>
        </div>
      </div>
    </div>
  </div>
</section>
</div>
"""

TESTIMONIALS_HTML = """
<div class="shiv-page">
<section class="shiv-test">
  <div class="shiv-wrap">
    <div class="test-hdr">
      <div>
        <div class="sec-tag">What Whitefield Parents Say</div>
        <h2>Trusted by hundreds of families across Whitefield.</h2>
      </div>
      <div class="test-rating">
        <span class="stars-lg">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
        <span class="rating-txt">4.9 &middot; Whitefield, ITPL, Kadugodi &amp; nearby</span>
      </div>
    </div>
    <div>
      <div class="carousel" id="shiv-carousel">
        <div class="t-card active">
          <div class="tcard-in">
            <div class="tquote">&ldquo;</div>
            <div class="tstars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
            <div class="theadline">Finally, a world-class pediatrician right in Whitefield.</div>
            <p class="ttext">We used to drive all the way to Koramangala for our daughter&rsquo;s pediatrician. After we found Dr. Diggikar at Medicover Whitefield, those long drives are over. His UK training and experience show in every consultation. He&rsquo;s now our family&rsquo;s go-to doctor for both our kids.</p>
            <div class="tauthor"><div class="tavatar">AK</div><div><div class="tname">Anjali &amp; Karthik</div><div class="tloc">Whitefield &middot; near Forum Mall</div></div></div>
          </div>
        </div>
        <div class="t-card">
          <div class="tcard-in">
            <div class="tquote">&ldquo;</div>
            <div class="tstars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
            <div class="theadline">Top pediatrician near ITPL &mdash; no contest.</div>
            <p class="ttext">As working parents at ITPL, we needed a pediatrician close to work for emergencies. Dr. Diggikar at Medicover Whitefield is just 10 minutes away. He&rsquo;s handled everything from our son&rsquo;s vaccinations to a scary high fever episode at 2 months old. Can&rsquo;t recommend him enough.</p>
            <div class="tauthor"><div class="tavatar">PR</div><div><div class="tname">Priya R.</div><div class="tloc">ITPL</div></div></div>
          </div>
        </div>
        <div class="t-card">
          <div class="tcard-in">
            <div class="tquote">&ldquo;</div>
            <div class="tstars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
            <div class="theadline">Our Kadugodi neighborhood&rsquo;s most trusted children&rsquo;s doctor.</div>
            <p class="ttext">Everyone in our apartment complex in Kadugodi takes their kids to Dr. Diggikar. His NICU expertise saved our neighbor&rsquo;s premature twins, and he&rsquo;s been our son&rsquo;s pediatrician since birth. We drive 15 minutes to Medicover Whitefield every time &mdash; worth it.</p>
            <div class="tauthor"><div class="tavatar">RM</div><div><div class="tname">Rohan M.</div><div class="tloc">Kadugodi</div></div></div>
          </div>
        </div>
        <div class="t-card">
          <div class="tcard-in">
            <div class="tquote">&ldquo;</div>
            <div class="tstars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
            <div class="theadline">Asthma management expert &mdash; our daughter breathes easier now.</div>
            <p class="ttext">Our 7-year-old has severe asthma triggered by Bangalore&rsquo;s pollution. Dr. Diggikar created a detailed action plan, taught us proper inhaler technique, and her emergency visits dropped to zero. We live in Varthur and drive to Whitefield specifically to see him.</p>
            <div class="tauthor"><div class="tavatar">DS</div><div><div class="tname">Deepak S.</div><div class="tloc">Varthur</div></div></div>
          </div>
        </div>
        <div class="t-card">
          <div class="tcard-in">
            <div class="tquote">&ldquo;</div>
            <div class="tstars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
            <div class="theadline">No more rushing across Bangalore for pediatric emergencies.</div>
            <p class="ttext">Having a London-trained neonatologist and pediatrician right here in Whitefield gives us so much peace of mind. Dr. Diggikar is available 24/7 at Medicover for emergencies, and his team has handled our twins&rsquo; illnesses expertly every single time.</p>
            <div class="tauthor"><div class="tavatar">SA</div><div><div class="tname">Sneha &amp; Arjun</div><div class="tloc">Brookefield</div></div></div>
          </div>
        </div>
      </div>
      <div class="carousel-nav">
        <button class="c-btn" id="shiv-prev" aria-label="Previous">&#8249;</button>
        <div class="c-dots" id="shiv-dots"></div>
        <button class="c-btn" id="shiv-next" aria-label="Next">&#8250;</button>
      </div>
    </div>
  </div>
</section>
</div>
"""

FAQ_HTML = """
<div class="shiv-page">
<section class="shiv-faq">
  <div class="shiv-wrap">
    <div class="sec-tag">Frequently Asked</div>
    <h2>Answers for parents in Whitefield, ITPL &amp; nearby.</h2>
    <div class="faq-layout">
      <aside class="faq-sidebar">
        <div class="faq-side-card">
          <h3>Have another question?</h3>
          <p>Speak to our team during clinic hours, or call anytime for pediatric emergencies &mdash; 24/7 at Medicover Whitefield.</p>
          <a href="tel:+919133555335" class="btn btn-white"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.27h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 9a16 16 0 0 0 6 6l1.09-1.09a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>+91-9133555335</a>
        </div>
      </aside>
      <div class="faq-list">
        <div class="faq-item is-open">
          <button class="faq-q" aria-expanded="true"><span>Is Dr. Diggikar&rsquo;s clinic located inside Whitefield or do I need to travel far?</span><span class="faq-qi">+</span></button>
          <div class="faq-a open"><p>Dr. Diggikar practices at Medicover Women &amp; Children Hospital on Whitefield Main Road &mdash; right in the heart of Whitefield, 5 minutes from Forum Neighbourhood Mall and 10 minutes from ITPL. Most families from Whitefield, Kadugodi, Varthur, Hoodi, and Brookefield reach the hospital in 10&ndash;15 minutes by car. You do <strong>not</strong> need to travel to Koramangala, Indiranagar, or other parts of Bangalore.</p></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false"><span>Can I walk in for consultations or do I need to book an appointment?</span><span class="faq-qi">+</span></button>
          <div class="faq-a"><p>Walk-in consultations are accepted for sick child visits and urgent concerns during clinic hours (Mon&ndash;Sat, 9:30 AM &ndash; 2:30 PM). For routine check-ups, vaccinations, and non-urgent consultations, we recommend booking. Book online at <a href="https://www.medicoverhospitals.in/doctors/dr-shivashankar-diggikar" target="_blank" rel="noopener">medicoverhospitals.in</a> or call <a href="tel:+919133555335">+91-9133555335</a>.</p></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false"><span>What age children does Dr. Diggikar treat at Medicover Whitefield?</span><span class="faq-qi">+</span></button>
          <div class="faq-a"><p>Dr. Diggikar treats children from newborn (day 0) through 18 years (adolescence). As a neonatologist, he specializes in the critical first 28 days of life including NICU care for premature babies. Many Whitefield families have been with Dr. Diggikar since their child&rsquo;s birth.</p></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false"><span>Does Dr. Diggikar provide vaccinations at the Whitefield clinic?</span><span class="faq-qi">+</span></button>
          <div class="faq-a"><p>Yes. Dr. Diggikar follows the IAP 2025 vaccination schedule and provides all mandatory and optional vaccines at Medicover Whitefield. This includes BCG, Hepatitis B, DPT, Polio, MMR, Varicella, Rotavirus, Pneumococcal conjugate, Meningococcal, Typhoid, Influenza, and HPV vaccines.</p></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false"><span>Is Dr. Diggikar available for pediatric emergencies in Whitefield?</span><span class="faq-qi">+</span></button>
          <div class="faq-a"><p>Yes. Dr. Diggikar provides 24/7 on-call pediatric emergency consultation at Medicover Whitefield. For emergencies like high fever in infants under 3 months, severe dehydration, breathing difficulty, or seizures &mdash; call <a href="tel:+919133555335">+91-9133555335</a> or go directly to Medicover Whitefield Emergency.</p></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false"><span>Does Medicover Whitefield accept health insurance for pediatric care?</span><span class="faq-qi">+</span></button>
          <div class="faq-a"><p>Yes. Medicover Hospitals Whitefield is empaneled with all major health insurance providers including Star Health, HDFC Ergo, ICICI Lombard, Max Bupa, Care Health, Religare, Bajaj Allianz, New India Assurance, and government schemes like Ayushman Bharat and Karnataka Arogya Sanjeevani.</p></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false"><span>What makes Dr. Diggikar one of the top pediatricians in Whitefield?</span><span class="faq-qi">+</span></button>
          <div class="faq-a"><p>Dr. Diggikar is one of the few FRCPCH (UK) and FRCPI (Ireland) certified pediatricians practicing full-time in Whitefield. His London training at Homerton University Hospital, 30+ research publications, Associate Editor role at BMJ Paediatrics Open, and Director-level position at Medicover Whitefield set him apart significantly from most local pediatricians.</p></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false"><span>Can Dr. Diggikar help with childhood asthma and allergies common in Whitefield?</span><span class="faq-qi">+</span></button>
          <div class="faq-a"><p>Yes. Dr. Diggikar has extensive experience managing childhood asthma, wheezing, allergic rhinitis, eczema, and food allergies &mdash; conditions increasingly common in Whitefield and ITPL areas due to Bangalore&rsquo;s air pollution. He creates personalized asthma action plans and teaches proper inhaler/spacer technique to parents.</p></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false"><span>Is there parking available at the Whitefield clinic?</span><span class="faq-qi">+</span></button>
          <div class="faq-a"><p>Yes. Medicover Women &amp; Children Hospital, Whitefield has ample free parking available for patients. The hospital is easily accessible by car with dedicated parking bays, and well-known to local auto drivers as &ldquo;Medicover Hospital, Whitefield Main Road&rdquo;.</p></div>
        </div>
        <div class="faq-item">
          <button class="faq-q" aria-expanded="false"><span>Can I consult Dr. Diggikar for my newborn baby in Whitefield?</span><span class="faq-qi">+</span></button>
          <div class="faq-a"><p>Absolutely. As a London-trained neonatologist, Dr. Diggikar specializes in newborn care including jaundice management, feeding problems, low birth weight babies, premature infants, and NICU admissions. Many Whitefield families deliver at Medicover Whitefield specifically to have Dr. Diggikar attend the delivery and provide immediate newborn care.</p></div>
        </div>
      </div>
    </div>
  </div>
</section>
</div>
"""

CTA_HTML = """
<div class="shiv-page">
<section class="shiv-cta">
  <div class="shiv-wrap">
    <div class="cta-in">
      <div class="sec-tag-w">Book an Appointment</div>
      <h2>Expert Pediatric Care Right Here in Whitefield, Bangalore.</h2>
      <p class="cta-desc">No need to travel across Bangalore for UK-certified pediatric expertise. Dr. Shivashankar Diggikar brings FRCPCH (UK), FRCPI (Ireland) training, 15+ years of experience, and London-trained neonatal care right to your neighborhood at Medicover Women &amp; Children Hospital, Whitefield.</p>
      <div class="cta-btns">
        <a href="https://www.medicoverhospitals.in/doctors/dr-shivashankar-diggikar" target="_blank" rel="noopener" class="btn btn-white"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>Book Appointment Online</a>
        <a href="tel:+919133555335" class="btn btn-ghost"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.27h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 9a16 16 0 0 0 6 6l1.09-1.09a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>Call: +91-9133555335</a>
      </div>
      <div class="cta-trust">
        <span class="cta-trust-item"><span class="cta-trust-icon"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></span>Medicover Whitefield, Bangalore</span>
        <span class="cta-trust-item"><span class="cta-trust-icon"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></span>Mon&ndash;Sat, 9:30 AM &ndash; 2:30 PM</span>
        <span class="cta-trust-item"><span class="cta-trust-icon"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></span>24/7 Pediatric Emergency</span>
      </div>
      <p class="cta-areas">Serving families in Whitefield &middot; ITPL &middot; Kadugodi &middot; Varthur &middot; Hoodi &middot; Brookefield &middot; Marathahalli &middot; Channasandra &middot; Nallurhalli &middot; Doddanekkundi.</p>
    </div>
  </div>
</section>
</div>
"""

MOBILE_CTA_AND_SCRIPTS = """
<div class="shiv-page">
<!-- Mobile Sticky CTA -->
<div class="mobile-sticky-cta" id="shiv-mobile-cta">
  <a href="tel:+919133555335" class="btn btn-outline-blue"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.27h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 9a16 16 0 0 0 6 6l1.09-1.09a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>Call Now</a>
  <a href="https://www.medicoverhospitals.in/doctors/dr-shivashankar-diggikar" target="_blank" rel="noopener" class="btn btn-primary"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>Book</a>
</div>

<script>
(function(){
  // Fonts
  if(!document.getElementById('shiv-fonts')){
    var l=document.createElement('link');
    l.id='shiv-fonts';
    l.rel='stylesheet';
    l.href='https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600;12..96,700;12..96,800&family=Inter:wght@300;400;500;600;700;800&display=swap';
    document.head.appendChild(l);
  }

  // FAQ accordion
  document.querySelectorAll('.faq-q').forEach(function(btn){
    btn.addEventListener('click',function(){
      var item=btn.closest('.faq-item');
      var ans=btn.nextElementSibling;
      var isOpen=item.classList.contains('is-open');
      document.querySelectorAll('.faq-item').forEach(function(el){
        el.classList.remove('is-open');
        el.querySelector('.faq-q').setAttribute('aria-expanded','false');
        el.querySelector('.faq-a').classList.remove('open');
      });
      if(!isOpen){
        item.classList.add('is-open');
        btn.setAttribute('aria-expanded','true');
        ans.classList.add('open');
      }
    });
  });

  // Carousel
  var cards=document.querySelectorAll('.t-card');
  var dotsEl=document.getElementById('shiv-dots');
  var cur=0,timer;
  if(cards.length&&dotsEl){
    cards.forEach(function(_,i){
      var d=document.createElement('button');
      d.className='c-dot'+(i===0?' active':'');
      d.setAttribute('aria-label','Testimonial '+(i+1));
      d.addEventListener('click',function(){goTo(i);});
      dotsEl.appendChild(d);
    });
    function goTo(idx){
      cards[cur].classList.remove('active');
      dotsEl.querySelectorAll('.c-dot')[cur].classList.remove('active');
      cur=(idx+cards.length)%cards.length;
      cards[cur].classList.add('active');
      dotsEl.querySelectorAll('.c-dot')[cur].classList.add('active');
      clearInterval(timer);timer=setInterval(function(){goTo(cur+1);},6500);
    }
    var prev=document.getElementById('shiv-prev'),next=document.getElementById('shiv-next');
    if(prev)prev.addEventListener('click',function(){goTo(cur-1);});
    if(next)next.addEventListener('click',function(){goTo(cur+1);});
    var tx=0,el=document.getElementById('shiv-carousel');
    if(el){
      el.addEventListener('touchstart',function(e){tx=e.touches[0].clientX;},{passive:true});
      el.addEventListener('touchend',function(e){var d=tx-e.changedTouches[0].clientX;if(Math.abs(d)>50)goTo(d>0?cur+1:cur-1);});
    }
    timer=setInterval(function(){goTo(cur+1);},6500);
  }

  // Scroll reveal
  var ro=new IntersectionObserver(function(entries){
    entries.forEach(function(e){if(e.isIntersecting){e.target.classList.add('visible');ro.unobserve(e.target);}});
  },{threshold:0.08});
  document.querySelectorAll('.why-card,.svc-card,.loc-main,.faq-item,.hi-item,.cred-item').forEach(function(el){
    el.classList.add('reveal');ro.observe(el);
  });
})();
</script>
</div>
"""

# ── BUILD ELEMENTOR JSON ──────────────────────────────────────────────────────

def make_section(bg_color, html_content, padding_top="0", padding_bottom="0", stretch=True):
    """Create an Elementor section with a single HTML widget."""
    return {
        "id": uid(),
        "elType": "section",
        "isInner": False,
        "settings": {
            "stretch_section": "section-stretched" if stretch else "",
            "layout": "full_width",
            "content_width": {"unit": "px", "size": 1160, "sizes": []},
            "gap": "no",
            "padding": {
                "unit": "px",
                "top": padding_top,
                "right": "0",
                "bottom": padding_bottom,
                "left": "0",
                "isLinked": False
            },
            "background_background": "classic",
            "background_color": bg_color
        },
        "elements": [{
            "id": uid(),
            "elType": "column",
            "isInner": False,
            "settings": {
                "_column_size": 100,
                "_inline_size": None,
                "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
            },
            "elements": [{
                "id": uid(),
                "elType": "widget",
                "widgetType": "html",
                "settings": {
                    "html": html_content
                }
            }]
        }]
    }

# Google Fonts + CSS injection (invisible section, 0 height)
CSS_INJECT = f"""<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600;12..96,700;12..96,800&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style id="shiv-styles">{CSS}</style>"""

template = {
    "version": "0.4",
    "title": "Top Pediatrician Whitefield - Dr. Shivashankar Diggikar",
    "type": "page",
    "content": [
        make_section("transparent", CSS_INJECT, "0", "0"),
        make_section("#0a2540", HERO_HTML, "0", "0"),
        make_section("#ffffff", ABOUT_HTML, "0", "0"),
        make_section("#0a2540", WHY_HTML, "0", "0"),
        make_section("#f0f8ff", SERVICES_HTML, "0", "0"),
        make_section("#ffffff", LOCATION_HTML, "0", "0"),
        make_section("#f8fafc", TESTIMONIALS_HTML, "0", "0"),
        make_section("#ffffff", FAQ_HTML, "0", "0"),
        make_section("#0a2540", CTA_HTML, "0", "0"),
        make_section("transparent", MOBILE_CTA_AND_SCRIPTS, "0", "0"),
    ],
    "page_settings": {
        "custom_css": ""
    }
}

output_path = "/home/claude/repo/elementor-template.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(template, f, ensure_ascii=False, indent=2)

print(f"Generated: {output_path}")
print(f"File size: {len(json.dumps(template, ensure_ascii=False)):,} bytes")
print(f"Sections: {len(template['content'])}")
