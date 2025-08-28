"use client"

import { useState, useEffect } from 'react'
import { ChevronDown, ChevronUp, TrendingUp, Shield, Globe, Star, Users, DollarSign, Award, Clock } from 'lucide-react'

// Pricing plans data
const pricingPlans = [
  {
    name: "Starter",
    price: "$99",
    period: "one-time",
    features: ["$10,000 Account", "10% Profit Target", "5% Max Drawdown", "1:100 Leverage"],
    popular: false
  },
  {
    name: "Standard", 
    price: "$199",
    period: "one-time",
    features: ["$25,000 Account", "8% Profit Target", "5% Max Drawdown", "1:100 Leverage"],
    popular: true
  },
  {
    name: "Professional",
    price: "$399", 
    period: "one-time",
    features: ["$50,000 Account", "8% Profit Target", "5% Max Drawdown", "1:100 Leverage"],
    popular: false
  },
  {
    name: "Elite",
    price: "$799",
    period: "one-time", 
    features: ["$100,000 Account", "8% Profit Target", "5% Max Drawdown", "1:100 Leverage"],
    popular: false
  }
]

// FAQ data
const faqData = [
  {
    question: "What is a prop firm?",
    answer: "A proprietary trading firm provides capital to traders to trade financial markets in exchange for a share of the profits."
  },
  {
    question: "How does the evaluation work?",
    answer: "Our evaluation process consists of a single phase where you need to achieve the profit target while staying within the maximum drawdown limits."
  },
  {
    question: "What happens after I pass?",
    answer: "Once you pass the evaluation, you become a funded trader and can start trading with our capital while keeping up to 90% of the profits."
  },
  {
    question: "Are there any time limits?",
    answer: "No, we don't have any time limits on our challenges. Trade at your own pace and develop your strategy without pressure."
  }
]

export default function FxologyPage() {
  const [activeStep, setActiveStep] = useState(1)
  const [openFaq, setOpenFaq] = useState<number | null>(null)
  const [countdown, setCountdown] = useState({
    days: 7,
    hours: 23,
    minutes: 45,
    seconds: 30
  })

  // Countdown timer effect
  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown(prev => {
        let { days, hours, minutes, seconds } = prev
        
        if (seconds > 0) {
          seconds--
        } else if (minutes > 0) {
          minutes--
          seconds = 59
        } else if (hours > 0) {
          hours--
          minutes = 59
          seconds = 59
        } else if (days > 0) {
          days--
          hours = 23
          minutes = 59
          seconds = 59
        }
        
        return { days, hours, minutes, seconds }
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  return (
    <div className="min-h-screen bg-[#08090A] text-white overflow-hidden" style={{ fontFamily: 'Inter, sans-serif' }}>
      {/* Digital Matrix Flow Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        {/* Floating Numbers and Equations */}
        <div className="absolute inset-0">
          {[...Array(30)].map((_, i) => (
            <div
              key={i}
              className="absolute text-gray-600/30 text-sm font-mono animate-float"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 10}s`,
                animationDuration: `${15 + Math.random() * 10}s`
              }}
            >
              {Math.random() > 0.5 ? `${Math.floor(Math.random() * 20)}+${Math.floor(Math.random() * 20)}` : `$${Math.floor(Math.random() * 999)}K`}
            </div>
          ))}
        </div>

        {/* Additional Particle Effects */}
        <div className="absolute inset-0">
          {[...Array(15)].map((_, i) => (
            <div
              key={`particle-${i}`}
              className="absolute w-1 h-1 bg-gray-500/20 rounded-full animate-particle-drift"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 12}s`,
                animationDuration: `${10 + Math.random() * 8}s`
              }}
            />
          ))}
        </div>

        {/* Enhanced Grid Overlay */}
        <div className="absolute inset-0 opacity-5" style={{
          backgroundImage: 'linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)',
          backgroundSize: '50px 50px'
        }}></div>
        
        {/* Pulsing Dots */}
        <div className="absolute inset-0">
          {[...Array(8)].map((_, i) => (
            <div
              key={`dot-${i}`}
              className="absolute w-2 h-2 bg-gray-400/20 rounded-full animate-pulse"
              style={{
                left: `${10 + (i * 12)}%`,
                top: `${20 + Math.sin(i) * 30}%`,
                animationDelay: `${i * 0.5}s`,
                animationDuration: `${2 + Math.random() * 1}s`
              }}
            />
          ))}
        </div>
        
        {/* Data Streams */}
        <div className="absolute inset-0">
          <div className="absolute top-1/4 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-[#9CA3AF]/30 to-transparent animate-pulse"></div>
          <div className="absolute top-3/4 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-[#9CA3AF]/20 to-transparent animate-pulse delay-1000"></div>
          <div className="absolute left-1/4 top-0 w-0.5 h-full bg-gradient-to-b from-transparent via-[#9CA3AF]/20 to-transparent animate-pulse delay-500"></div>
          <div className="absolute left-3/4 top-0 w-0.5 h-full bg-gradient-to-b from-transparent via-[#9CA3AF]/15 to-transparent animate-pulse delay-1500"></div>
        </div>
      </div>

      {/* Header */}
      <header className="relative z-10 border-b border-gray-800/50 backdrop-blur-sm">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <TrendingUp className="h-8 w-8 text-[#9CA3AF] animate-pulse" />
              <h1 className="text-2xl font-bold text-white">Fxology</h1>
            </div>
            <nav className="hidden md:flex items-center space-x-8">
              <a href="#" className="text-gray-300 hover:text-[#9CA3AF] transition-colors">Home</a>
              <a href="#" className="text-gray-300 hover:text-[#9CA3AF] transition-colors">About</a>
              <a href="#" className="text-gray-300 hover:text-[#9CA3AF] transition-colors">Pricing</a>
              <a href="#" className="text-gray-300 hover:text-[#9CA3AF] transition-colors">FAQ</a>
              <button className="bg-[#9CA3AF] text-white px-6 py-2 rounded-lg font-semibold hover:bg-[#6B7280] transition-all duration-300 transform hover:scale-105">
                Start Challenge
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative z-10 flex items-center justify-center min-h-screen px-6">
        <div className="text-center max-w-4xl mx-auto">
          <div className="space-y-6">
            <h1 className="text-6xl md:text-7xl lg:text-8xl font-bold text-white leading-tight animate-kinetic-reveal">
              No Time Limit
              <br />
              <span className="text-[#9CA3AF] animate-pulse">Prop Firm</span>
            </h1>
            <p className="text-2xl md:text-3xl text-gray-300 font-medium animate-kinetic-reveal delay-300">
              Conquer the market
            </p>
            <div className="pt-8 animate-kinetic-reveal delay-500">
              <button className="bg-[#9CA3AF] text-white px-12 py-4 rounded-lg text-xl font-bold hover:bg-[#6B7280] transform hover:scale-105 transition-all duration-300 shadow-[0_0_30px_rgba(156,163,175,0.3)] animate-breathing">
                Start a challenge
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof Metrics Section */}
      <section className="relative z-10 py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center animate-counter-bounce">
              <div className="text-4xl md:text-5xl font-bold text-[#9CA3AF] mb-2">$400K+</div>
              <p className="text-gray-400">Paid out to Traders</p>
            </div>
            <div className="text-center animate-counter-bounce delay-300">
              <div className="text-4xl md:text-5xl font-bold text-[#9CA3AF] mb-2">15K+</div>
              <p className="text-gray-400">Active Traders</p>
            </div>
            <div className="text-center animate-counter-bounce delay-500">
              <div className="text-4xl md:text-5xl font-bold text-[#9CA3AF] mb-2">150+</div>
              <p className="text-gray-400">Countries</p>
            </div>
            <div className="text-center animate-counter-bounce delay-700">
              <div className="text-4xl md:text-5xl font-bold text-[#9CA3AF] mb-2">99.2%</div>
              <p className="text-gray-400">Uptime</p>
            </div>
          </div>
        </div>
      </section>

      {/* How Does It Work Section */}
      <section className="relative z-10 py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-4xl md:text-5xl font-bold text-center text-white mb-16">How Does It Work?</h2>
          
          {/* Waveform Background */}
          <div className="relative overflow-hidden rounded-2xl bg-gray-900/30 backdrop-blur-sm border border-gray-800">
            <svg className="absolute inset-0 w-full h-full opacity-20" viewBox="0 0 400 200">
              <path
                d="M0,100 Q100,50 200,100 T400,100"
                stroke="#9CA3AF"
                strokeWidth="2"
                fill="none"
                className="animate-wave"
              />
              <path
                d="M0,120 Q150,80 300,120 T600,120"
                stroke="#9CA3AF"
                strokeWidth="1"
                fill="none"
                opacity="0.6"
                className="animate-wave-delayed"
              />
            </svg>
            
            <div className="relative z-10 p-8">
              {/* Step Navigation */}
              <div className="flex justify-center mb-12">
                <div className="flex space-x-8">
                  {[1, 2, 3].map((step) => (
                    <button
                      key={step}
                      onClick={() => setActiveStep(step)}
                      className={`px-6 py-3 rounded-lg font-semibold transition-all transform hover:scale-105 ${
                        activeStep === step
                          ? 'bg-[#9CA3AF] text-white animate-pulse'
                          : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                      }`}
                    >
                      Step {step}
                    </button>
                  ))}
                </div>
              </div>
              
              {/* Step Content */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div className="space-y-6">
                  {activeStep === 1 && (
                    <>
                      <h3 className="text-3xl font-bold text-white">Choose Your Challenge</h3>
                      <p className="text-gray-300 text-lg leading-relaxed">
                        Select from our range of trading challenges based on your experience level and risk tolerance. 
                        From $10K to $100K accounts, all with no time limits.
                      </p>
                      <ul className="space-y-2 text-gray-400">
                        <li>• Multiple account sizes available</li>
                        <li>• Flexible profit targets</li>
                        <li>• No time pressure</li>
                      </ul>
                    </>
                  )}
                  {activeStep === 2 && (
                    <>
                      <h3 className="text-3xl font-bold text-white">Trade & Prove Your Skills</h3>
                      <p className="text-gray-300 text-lg leading-relaxed">
                        Demonstrate your trading skills by reaching the profit target while staying within 
                        the maximum drawdown limits. Trade at your own pace with our advanced platform.
                      </p>
                      <ul className="space-y-2 text-gray-400">
                        <li>• Real market conditions</li>
                        <li>• Professional trading tools</li>
                        <li>• Risk management focus</li>
                      </ul>
                    </>
                  )}
                  {activeStep === 3 && (
                    <>
                      <h3 className="text-3xl font-bold text-white">Get Funded & Keep 90%</h3>
                      <p className="text-gray-300 text-lg leading-relaxed">
                        Once you pass the evaluation, receive a funded account and keep up to 90% of your profits. 
                        Scale your account based on consistent performance.
                      </p>
                      <ul className="space-y-2 text-gray-400">
                        <li>• Keep up to 90% of profits</li>
                        <li>• Monthly payouts</li>
                        <li>• Account scaling opportunities</li>
                      </ul>
                    </>
                  )}
                </div>
                
                <div className="flex justify-center">
                  <div className="w-96 h-64 bg-gray-800/50 rounded-xl border border-gray-700 flex items-center justify-center">
                    <div className="text-gray-400 text-center">
                      <div className="w-16 h-16 bg-[#9CA3AF]/20 rounded-full flex items-center justify-center mx-auto mb-4 animate-spin-slow">
                        {activeStep === 1 && <DollarSign className="h-8 w-8 text-[#9CA3AF]" />}
                        {activeStep === 2 && <TrendingUp className="h-8 w-8 text-[#9CA3AF]" />}
                        {activeStep === 3 && <Award className="h-8 w-8 text-[#9CA3AF]" />}
                      </div>
                      <p>Step {activeStep} Visualization</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Payouts & Certificates Section */}
      <section className="relative z-10 py-20 px-6">
        <div className="container mx-auto max-w-4xl">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-center">
            <div className="text-center lg:text-right">
              <h2 className="text-4xl font-bold text-white mb-4">Payouts</h2>
              <p className="text-gray-400">Real money, real results</p>
            </div>
            
            <div className="flex justify-center">
              <div className="relative group">
                {/* Wireframe Grid Background */}
                <div className="absolute inset-0 opacity-30 transform rotate-45 scale-110 animate-spin-very-slow">
                  <div className="grid grid-cols-8 grid-rows-8 gap-1 w-full h-full">
                    {[...Array(64)].map((_, i) => (
                      <div key={i} className="border border-[#9CA3AF]/20"></div>
                    ))}
                  </div>
                </div>
                
                {/* Certificate Card */}
                <div className="relative bg-gray-900/40 backdrop-blur-sm border border-gray-700/50 rounded-2xl p-8 transform group-hover:scale-105 transition-all duration-500 shadow-[0_0_50px_rgba(156,163,175,0.1)] animate-card-float">
                  <div className="text-center space-y-4">
                    <div className="w-16 h-16 bg-[#9CA3AF]/20 rounded-full flex items-center justify-center mx-auto animate-pulse">
                      <Award className="h-8 w-8 text-[#9CA3AF]" />
                    </div>
                    <h3 className="text-xl font-bold text-white">Payout Certificate</h3>
                    <div className="text-2xl font-bold text-[#9CA3AF]">$12,500</div>
                    <p className="text-gray-400 text-sm">Monthly Payout</p>
                    <div className="pt-4 border-t border-gray-700">
                      <p className="text-xs text-gray-500">Certified Trader Program</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="text-center lg:text-left">
              <h2 className="text-4xl font-bold text-white mb-4">Certificates</h2>
              <p className="text-gray-400">Verified achievements</p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Plans Section */}
      <section className="relative z-10 py-20 px-6">
        <div className="container mx-auto max-w-7xl">
          <h2 className="text-4xl md:text-5xl font-bold text-center text-white mb-16">Choose Your Challenge</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {pricingPlans.map((plan, index) => (
              <div
                key={index}
                className={`relative group cursor-pointer transition-all duration-300 transform hover:scale-105 ${
                  plan.popular ? 'lg:-mt-4' : ''
                }`}
              >
                {/* Glassmorphism Card */}
                <div className={`relative bg-gray-900/40 backdrop-blur-sm border rounded-2xl p-6 h-full transition-all duration-300 animate-card-bounce ${
                  plan.popular
                    ? 'border-[#9CA3AF] shadow-[0_0_30px_rgba(156,163,175,0.2)]'
                    : 'border-gray-700/50 group-hover:border-[#9CA3AF] group-hover:shadow-[0_0_30px_rgba(156,163,175,0.1)]'
                }`}>
                  {plan.popular && (
                    <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                      <div className="bg-[#9CA3AF] text-white px-4 py-1 rounded-full text-sm font-semibold animate-pulse">
                        Most Popular
                      </div>
                    </div>
                  )}
                  
                  <div className="text-center space-y-6">
                    <h3 className="text-2xl font-bold text-white">{plan.name}</h3>
                    <div>
                      <span className="text-4xl font-bold text-[#9CA3AF]">{plan.price}</span>
                      <span className="text-gray-400 ml-2">{plan.period}</span>
                    </div>
                    
                    <ul className="space-y-3 text-left">
                      {plan.features.map((feature, idx) => (
                        <li key={idx} className="flex items-center text-gray-300">
                          <div className="w-2 h-2 bg-[#9CA3AF] rounded-full mr-3 animate-pulse"></div>
                          {feature}
                        </li>
                      ))}
                    </ul>
                    
                    <button className={`w-full py-3 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 ${
                      plan.popular
                        ? 'bg-[#9CA3AF] text-white hover:bg-[#6B7280] animate-breathing'
                        : 'bg-gray-800 text-white group-hover:bg-[#9CA3AF] group-hover:text-white'
                    }`}>
                      Start Challenge
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA & Countdown Section */}
      <section className="relative z-10 py-20 px-6">
        <div className="container mx-auto max-w-4xl text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Traders from more than 150 countries trust Fxology
          </h2>
          <p className="text-gray-400 text-lg mb-12">
            Join thousands of successful traders who have already started their journey with us
          </p>
          
          {/* Countdown Timer */}
          <div className="mb-12">
            <p className="text-[#9CA3AF] text-sm font-semibold mb-4 animate-pulse">LIMITED TIME OFFER ENDS IN:</p>
            <div className="flex justify-center space-x-8">
              <div className="text-center animate-counter-bounce">
                <div className="text-4xl md:text-5xl font-bold text-white mb-2">{countdown.days.toString().padStart(2, '0')}</div>
                <div className="text-gray-400 text-sm">DAYS</div>
              </div>
              <div className="text-center animate-counter-bounce">
                <div className="text-4xl md:text-5xl font-bold text-white mb-2">{countdown.hours.toString().padStart(2, '0')}</div>
                <div className="text-gray-400 text-sm">HOURS</div>
              </div>
              <div className="text-center animate-counter-bounce">
                <div className="text-4xl md:text-5xl font-bold text-white mb-2">{countdown.minutes.toString().padStart(2, '0')}</div>
                <div className="text-gray-400 text-sm">MINUTES</div>
              </div>
              <div className="text-center animate-counter-bounce">
                <div className="text-4xl md:text-5xl font-bold text-white mb-2">{countdown.seconds.toString().padStart(2, '0')}</div>
                <div className="text-gray-400 text-sm">SECONDS</div>
              </div>
            </div>
          </div>
          
          {/* Planet Arc with Shooting Stars */}
          <div className="relative mb-12">
            <svg className="w-full h-32 opacity-30" viewBox="0 0 400 100">
              <defs>
                <linearGradient id="arcGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#9CA3AF" stopOpacity="0" />
                  <stop offset="50%" stopColor="#9CA3AF" stopOpacity="0.8" />
                  <stop offset="100%" stopColor="#9CA3AF" stopOpacity="0" />
                </linearGradient>
              </defs>
              <path
                d="M50,80 Q200,20 350,80"
                stroke="url(#arcGradient)"
                strokeWidth="2"
                fill="none"
              />
              {/* Shooting Stars */}
              <circle r="2" fill="#9CA3AF" opacity="0.8">
                <animateMotion dur="3s" repeatCount="indefinite">
                  <path d="M0,60 Q200,10 400,60" />
                </animateMotion>
              </circle>
              <circle r="1.5" fill="#9CA3AF" opacity="0.6">
                <animateMotion dur="4s" repeatCount="indefinite" begin="1s">
                  <path d="M0,70 Q200,15 400,70" />
                </animateMotion>
              </circle>
            </svg>
          </div>
          
          <button className="bg-[#9CA3AF] text-white px-12 py-4 rounded-lg text-xl font-bold hover:bg-[#6B7280] transform hover:scale-105 transition-all duration-300 shadow-[0_0_30px_rgba(156,163,175,0.3)] animate-breathing">
            Start Your Challenge Now
          </button>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="relative z-10 py-20 px-6">
        <div className="container mx-auto max-w-4xl">
          <h2 className="text-4xl md:text-5xl font-bold text-center text-white mb-16">Frequently Asked Questions</h2>
          
          <div className="space-y-4">
            {faqData.map((faq, index) => (
              <div key={index} className="bg-gray-900/40 backdrop-blur-sm border border-gray-700/50 rounded-xl overflow-hidden">
                <button
                  onClick={() => setOpenFaq(openFaq === index ? null : index)}
                  className="w-full px-6 py-6 text-left flex items-center justify-between hover:bg-gray-800/50 transition-colors"
                >
                  <span className="text-lg font-semibold text-white">{faq.question}</span>
                  <div className={`transform transition-transform duration-300 ${openFaq === index ? 'rotate-45' : ''}`}>
                    {openFaq === index ? (
                      <ChevronUp className="h-6 w-6 text-[#9CA3AF] animate-spin-slow" />
                    ) : (
                      <ChevronDown className="h-6 w-6 text-gray-400 hover:text-[#9CA3AF] transition-colors" />
                    )}
                  </div>
                </button>
                
                <div className={`overflow-hidden transition-all duration-300 ${
                  openFaq === index ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'
                }`}>
                  <div className="px-6 pb-6">
                    <p className="text-gray-300 leading-relaxed">{faq.answer}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Who We Are Section */}
      <section className="relative z-10 py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-16">
            <h2 className="text-5xl md:text-6xl font-bold text-white mb-8 animate-kinetic-reveal">
              Who we are?
            </h2>
            <h3 className="text-3xl md:text-4xl font-bold text-[#9CA3AF] animate-kinetic-reveal delay-300">
              And how it all started?
            </h3>
          </div>
          
          {/* Flowing Line Graph */}
          <div className="relative">
            <svg className="w-full h-64 opacity-60" viewBox="0 0 800 200">
              <defs>
                <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#9CA3AF" stopOpacity="0.2" />
                  <stop offset="50%" stopColor="#9CA3AF" stopOpacity="1" />
                  <stop offset="100%" stopColor="#9CA3AF" stopOpacity="0.2" />
                </linearGradient>
              </defs>
              
              {/* Main Chart Line */}
              <path
                d="M50,150 Q200,100 350,80 T750,60"
                stroke="url(#lineGradient)"
                strokeWidth="3"
                fill="none"
                className="animate-draw-line"
              />
              
              {/* Data Points */}
              <circle cx="200" cy="100" r="4" fill="#9CA3AF" opacity="0.8">
                <animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite" begin="1s" />
              </circle>
              <circle cx="350" cy="80" r="4" fill="#9CA3AF" opacity="0.8">
                <animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite" begin="1.5s" />
              </circle>
              <circle cx="500" cy="75" r="4" fill="#9CA3AF" opacity="0.8">
                <animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite" begin="2s" />
              </circle>
              
              {/* Floating Numbers */}
              <text x="200" y="90" fill="#9CA3AF" fontSize="12" textAnchor="middle" opacity="0.8">$2.5M</text>
              <text x="350" y="70" fill="#9CA3AF" fontSize="12" textAnchor="middle" opacity="0.8">$5.1M</text>
              <text x="500" y="65" fill="#9CA3AF" fontSize="12" textAnchor="middle" opacity="0.8">$8.7M</text>
            </svg>
          </div>
          
          <div className="max-w-3xl mx-auto text-center">
            <p className="text-xl text-gray-300 leading-relaxed mb-8">
              Founded by professional traders with over 15 years of combined experience in the financial markets, 
              Fxology was created to democratize access to trading capital and provide opportunities for skilled 
              traders worldwide.
            </p>
            <p className="text-lg text-gray-400">
              Our mission is to identify and fund talented traders while providing them with the tools, 
              support, and capital needed to succeed in today's dynamic financial markets.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-gray-800/50 bg-gray-900/20 backdrop-blur-sm">
        <div className="container mx-auto px-6 py-16">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Programs */}
            <div>
              <h4 className="text-lg font-semibold text-white mb-6">Programs</h4>
              <ul className="space-y-3">
                <li><a href="#" className="text-gray-400 hover:text-[#9CA3AF] transition-colors">Trading Challenges</a></li>
                <li><a href="#" className="text-gray-400 hover:text-[#9CA3AF] transition-colors">Funded Accounts</a></li>
                <li><a href="#" className="text-gray-400 hover:text-[#9CA3AF] transition-colors">Educational Resources</a></li>
                <li><a href="#" className="text-gray-400 hover:text-[#9CA3AF] transition-colors">Trading Platform</a></li>
              </ul>
            </div>
            
            {/* About Us */}
            <div>
              <h4 className="text-lg font-semibold text-white mb-6">About Us</h4>
              <ul className="space-y-3">
                <li><a href="#" className="text-gray-400 hover:text-[#9CA3AF] transition-colors">Our Story</a></li>
                <li><a href="#" className="text-gray-400 hover:text-[#9CA3AF] transition-colors">Team</a></li>
                <li><a href="#" className="text-gray-400 hover:text-[#9CA3AF] transition-colors">Careers</a></li>
                <li><a href="#" className="text-gray-400 hover:text-[#9CA3AF] transition-colors">Contact</a></li>
              </ul>
            </div>
            
            {/* Legal */}
            <div>
              <h4 className="text-lg font-semibold text-white mb-6">Legal</h4>
              <ul className="space-y-3">
                <li><a href="#" className="text-gray-400 hover:text-[#9CA3AF] transition-colors">Terms of Service</a></li>
                <li><a href="#" className="text-gray-400 hover:text-[#9CA3AF] transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="text-gray-400 hover:text-[#9CA3AF] transition-colors">Risk Disclosure</a></li>
                <li><a href="#" className="text-gray-400 hover:text-[#9CA3AF] transition-colors">Compliance</a></li>
              </ul>
            </div>
            
            {/* Social & Brand */}
            <div>
              <div className="flex items-center space-x-3 mb-6">
                <TrendingUp className="h-8 w-8 text-[#9CA3AF] animate-pulse" />
                <h4 className="text-2xl font-bold text-white">Fxology</h4>
              </div>
              <p className="text-gray-400 mb-6">Empowering traders worldwide with capital and opportunity.</p>
              <div className="flex space-x-4">
                <a href="#" className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-[#9CA3AF] hover:text-white transition-all transform hover:scale-110">
                  <Users className="h-5 w-5" />
                </a>
                <a href="#" className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-[#9CA3AF] hover:text-white transition-all transform hover:scale-110">
                  <Globe className="h-5 w-5" />
                </a>
                <a href="#" className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-[#9CA3AF] hover:text-white transition-all transform hover:scale-110">
                  <Shield className="h-5 w-5" />
                </a>
              </div>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-12 pt-8 text-center">
            <p className="text-gray-500">© 2024 Fxology. All rights reserved. Trading involves risk of loss.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}