"use client"

import { useState, useEffect, useRef } from 'react'
import { motion, useInView, useAnimation, useScroll, useTransform } from 'framer-motion'
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

// React Bits-inspired animation variants and easing functions
const easing = [0.6, -0.05, 0.01, 0.99]

const fadeInUp = {
  initial: { 
    opacity: 0, 
    y: 60,
    scale: 0.95
  },
  animate: { 
    opacity: 1, 
    y: 0,
    scale: 1,
    transition: {
      duration: 0.8,
      ease: easing
    }
  }
}

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.1
    }
  }
}

const staggerItem = {
  initial: { 
    opacity: 0, 
    y: 40,
    scale: 0.9
  },
  animate: { 
    opacity: 1, 
    y: 0,
    scale: 1,
    transition: {
      duration: 0.6,
      ease: easing
    }
  }
}

const textReveal = {
  initial: { 
    opacity: 0,
    y: 100,
    rotateX: 90
  },
  animate: { 
    opacity: 1,
    y: 0,
    rotateX: 0,
    transition: {
      duration: 0.8,
      ease: easing
    }
  }
}

const magneticHover = {
  scale: 1.05,
  transition: {
    type: "spring",
    stiffness: 400,
    damping: 10
  }
}

const cardHover = {
  y: -8,
  scale: 1.02,
  rotateX: 5,
  boxShadow: "0 20px 40px rgba(156, 163, 175, 0.1)",
  transition: {
    type: "spring",
    stiffness: 300,
    damping: 20
  }
}

// Intersection Observer hook for scroll animations
const useScrollAnimation = () => {
  const controls = useAnimation()
  const ref = useRef(null)
  const inView = useInView(ref, { once: true, amount: 0.1 })

  useEffect(() => {
    if (inView) {
      controls.start("animate")
    }
  }, [controls, inView])

  return { ref, controls }
}

export default function FxologyPage() {
  const [activeStep, setActiveStep] = useState(1)
  const [openFaq, setOpenFaq] = useState<number | null>(null)
  const [countdown, setCountdown] = useState({
    days: 7,
    hours: 23,
    minutes: 45,
    seconds: 30
  })

  const { scrollYProgress } = useScroll()
  const backgroundY = useTransform(scrollYProgress, [0, 1], ["0%", "100%"])
  const backgroundScale = useTransform(scrollYProgress, [0, 1], [1, 1.1])

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
      {/* Enhanced Digital Matrix Flow Background with Framer Motion */}
      <motion.div 
        className="fixed inset-0 overflow-hidden pointer-events-none"
        style={{ y: backgroundY, scale: backgroundScale }}
      >
        {/* Animated Floating Numbers and Equations */}
        <div className="absolute inset-0">
          {[...Array(30)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute text-gray-600/30 text-sm font-mono"
              initial={{ opacity: 0, y: 100 }}
              animate={{ 
                opacity: [0.3, 0.6, 0.3], 
                y: [100, -100],
                x: [0, Math.sin(i) * 50]
              }}
              transition={{
                duration: 15 + Math.random() * 10,
                repeat: Infinity,
                delay: Math.random() * 10,
                ease: "linear"
              }}
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
              }}
            >
              {Math.random() > 0.5 ? `${Math.floor(Math.random() * 20)}+${Math.floor(Math.random() * 20)}` : `$${Math.floor(Math.random() * 999)}K`}
            </motion.div>
          ))}
        </div>

        {/* Enhanced Particle Effects with Physics */}
        <div className="absolute inset-0">
          {[...Array(20)].map((_, i) => (
            <motion.div
              key={`particle-${i}`}
              className="absolute w-1 h-1 bg-gray-500/20 rounded-full"
              initial={{ opacity: 0, scale: 0 }}
              animate={{ 
                opacity: [0, 0.8, 0],
                scale: [0, 1, 0],
                x: [0, Math.cos(i) * 200],
                y: [0, Math.sin(i) * 200]
              }}
              transition={{
                duration: 8 + Math.random() * 4,
                repeat: Infinity,
                delay: Math.random() * 8,
                ease: [0.25, 0.46, 0.45, 0.94]
              }}
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
              }}
            />
          ))}
        </div>

        {/* Animated Grid with Pulse Effect */}
        <motion.div 
          className="absolute inset-0 opacity-5"
          animate={{ 
            opacity: [0.05, 0.15, 0.05]
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          style={{
            backgroundImage: 'linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)',
            backgroundSize: '50px 50px'
          }}
        />
        
        {/* Floating Data Streams with Wave Motion */}
        <div className="absolute inset-0">
          {[...Array(4)].map((_, i) => (
            <motion.div
              key={`stream-${i}`}
              className={`absolute ${i % 2 === 0 ? 'w-full h-0.5' : 'w-0.5 h-full'} bg-gradient-to-r from-transparent via-[#9CA3AF]/20 to-transparent`}
              style={{
                [i % 2 === 0 ? 'top' : 'left']: `${25 + (i * 25)}%`,
                [i % 2 === 0 ? 'left' : 'top']: '0%'
              }}
              animate={{
                opacity: [0.2, 0.6, 0.2],
                scaleX: i % 2 === 0 ? [0.8, 1.2, 0.8] : 1,
                scaleY: i % 2 !== 0 ? [0.8, 1.2, 0.8] : 1,
              }}
              transition={{
                duration: 3 + i,
                repeat: Infinity,
                delay: i * 0.5,
                ease: "easeInOut"
              }}
            />
          ))}
        </div>
      </motion.div>

      {/* Enhanced Header with Layout Animations */}
      <motion.header 
        className="relative z-10 border-b border-gray-800/50 backdrop-blur-sm"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: easing }}
      >
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <motion.div 
              className="flex items-center space-x-3"
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 400, damping: 10 }}
            >
              <motion.div
                animate={{ rotate: [0, 360] }}
                transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
              >
                <TrendingUp className="h-8 w-8 text-[#9CA3AF]" />
              </motion.div>
              <h1 className="text-2xl font-bold text-white">Fxology</h1>
            </motion.div>
            <nav className="hidden md:flex items-center space-x-8">
              {['Home', 'About', 'Pricing', 'FAQ'].map((item, index) => (
                <motion.a 
                  key={item}
                  href="#" 
                  className="text-gray-300 hover:text-[#9CA3AF] transition-colors relative"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1, duration: 0.4 }}
                  whileHover={{
                    scale: 1.1,
                    transition: { type: "spring", stiffness: 400, damping: 10 }
                  }}
                >
                  {item}
                  <motion.div
                    className="absolute -bottom-1 left-0 h-0.5 bg-[#9CA3AF]"
                    initial={{ width: 0 }}
                    whileHover={{ width: "100%" }}
                    transition={{ duration: 0.3 }}
                  />
                </motion.a>
              ))}
              <motion.button 
                className="bg-[#9CA3AF] text-white px-6 py-2 rounded-lg font-semibold relative overflow-hidden"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.5, duration: 0.4 }}
                whileHover={magneticHover}
                whileTap={{ scale: 0.95 }}
              >
                <motion.div
                  className="absolute inset-0 bg-gradient-to-r from-[#6B7280] to-[#9CA3AF]"
                  initial={{ x: "-100%" }}
                  whileHover={{ x: "100%" }}
                  transition={{ duration: 0.6 }}
                />
                <span className="relative z-10">Start Challenge</span>
              </motion.button>
            </nav>
          </div>
        </div>
      </motion.header>

      {/* Enhanced Hero Section with Text Reveal */}
      <section className="relative z-10 flex items-center justify-center min-h-screen px-6">
        <div className="text-center max-w-4xl mx-auto">
          <motion.div 
            className="space-y-6"
            initial="initial"
            animate="animate"
            variants={staggerContainer}
          >
            {/* Animated Headline with Character Reveal */}
            <div className="overflow-hidden">
              <motion.h1 
                className="text-6xl md:text-7xl lg:text-8xl font-bold text-white leading-tight"
                variants={textReveal}
              >
                {"No Time Limit".split("").map((char, index) => (
                  <motion.span
                    key={index}
                    initial={{ opacity: 0, y: 50, rotateX: 90 }}
                    animate={{ opacity: 1, y: 0, rotateX: 0 }}
                    transition={{
                      duration: 0.6,
                      delay: index * 0.05,
                      ease: easing
                    }}
                    className="inline-block"
                  >
                    {char === " " ? "\u00A0" : char}
                  </motion.span>
                ))}
                <br />
                <motion.span 
                  className="text-[#9CA3AF] inline-block"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.8, duration: 0.8, ease: easing }}
                >
                  {"Prop Firm".split("").map((char, index) => (
                    <motion.span
                      key={index}
                      initial={{ opacity: 0, y: 50 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{
                        duration: 0.6,
                        delay: 1 + index * 0.05,
                        ease: easing
                      }}
                      className="inline-block"
                    >
                      {char === " " ? "\u00A0" : char}
                    </motion.span>
                  ))}
                </motion.span>
              </motion.h1>
            </div>
            
            <motion.p 
              className="text-2xl md:text-3xl text-gray-300 font-medium"
              variants={fadeInUp}
              transition={{ delay: 1.5 }}
            >
              Conquer the market
            </motion.p>
            
            <motion.div 
              className="pt-8"
              variants={fadeInUp}
              transition={{ delay: 1.8 }}
            >
              <motion.button 
                className="bg-[#9CA3AF] text-white px-12 py-4 rounded-lg text-xl font-bold relative overflow-hidden shadow-[0_0_30px_rgba(156,163,175,0.3)]"
                whileHover={{
                  scale: 1.05,
                  boxShadow: "0 0 50px rgba(156, 163, 175, 0.5)",
                  transition: { duration: 0.3 }
                }}
                whileTap={{ scale: 0.95 }}
                animate={{
                  boxShadow: [
                    "0 0 30px rgba(156, 163, 175, 0.3)",
                    "0 0 50px rgba(156, 163, 175, 0.5)",
                    "0 0 30px rgba(156, 163, 175, 0.3)"
                  ]
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              >
                <motion.div
                  className="absolute inset-0 bg-gradient-to-r from-[#6B7280] via-[#9CA3AF] to-[#6B7280]"
                  initial={{ x: "-100%" }}
                  whileHover={{ x: "100%" }}
                  transition={{ duration: 0.8 }}
                />
                <span className="relative z-10">Start a challenge</span>
              </motion.button>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Enhanced Social Proof Metrics Section - "Meet Marvellous Insights" */}
      <section className="relative z-10 py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <motion.div
            className="grid grid-cols-2 md:grid-cols-4 gap-8"
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true, amount: 0.2 }}
          >
            {[
              { value: "$400K+", label: "Paid out to Traders", delay: 0 },
              { value: "15K+", label: "Active Traders", delay: 0.1 },
              { value: "150+", label: "Countries", delay: 0.2 },
              { value: "99.2%", label: "Uptime", delay: 0.3 }
            ].map((metric, index) => (
              <motion.div
                key={index}
                className="text-center group cursor-pointer"
                variants={staggerItem}
                whileHover={{
                  scale: 1.05,
                  y: -5,
                  transition: { type: "spring", stiffness: 400, damping: 10 }
                }}
              >
                <motion.div 
                  className="text-4xl md:text-5xl font-bold text-[#9CA3AF] mb-2 relative"
                  initial={{ opacity: 0, scale: 0.5 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ 
                    delay: metric.delay + 0.5,
                    duration: 0.8,
                    type: "spring",
                    stiffness: 200,
                    damping: 15
                  }}
                  viewport={{ once: true }}
                >
                  {metric.value}
                  <motion.div
                    className="absolute inset-0 bg-[#9CA3AF]/20 rounded-lg -z-10"
                    initial={{ scale: 0, opacity: 0 }}
                    whileInView={{ scale: 1, opacity: 1 }}
                    transition={{ delay: metric.delay + 0.8, duration: 0.6 }}
                    viewport={{ once: true }}
                  />
                </motion.div>
                <motion.p 
                  className="text-gray-400 group-hover:text-gray-300 transition-colors"
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: metric.delay + 0.7, duration: 0.6 }}
                  viewport={{ once: true }}
                >
                  {metric.label}
                </motion.p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Enhanced How Does It Work Section */}
      <section className="relative z-10 py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <motion.h2 
            className="text-4xl md:text-5xl font-bold text-center text-white mb-16"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: easing }}
            viewport={{ once: true }}
          >
            How Does It Work?
          </motion.h2>
          
          {/* Enhanced Waveform Background */}
          <motion.div 
            className="relative overflow-hidden rounded-2xl bg-gray-900/30 backdrop-blur-sm border border-gray-800"
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, ease: easing }}
            viewport={{ once: true }}
          >
            <svg className="absolute inset-0 w-full h-full opacity-20" viewBox="0 0 400 200">
              <motion.path
                d="M0,100 Q100,50 200,100 T400,100"
                stroke="#9CA3AF"
                strokeWidth="2"
                fill="none"
                initial={{ pathLength: 0, opacity: 0 }}
                whileInView={{ pathLength: 1, opacity: 1 }}
                transition={{ duration: 2, ease: "easeInOut" }}
                viewport={{ once: true }}
              />
              <motion.path
                d="M0,120 Q150,80 300,120 T600,120"
                stroke="#9CA3AF"
                strokeWidth="1"
                fill="none"
                opacity="0.6"
                initial={{ pathLength: 0 }}
                whileInView={{ pathLength: 1 }}
                transition={{ duration: 2.5, delay: 0.3, ease: "easeInOut" }}
                viewport={{ once: true }}
              />
            </svg>
            
            <div className="relative z-10 p-8">
              {/* Enhanced Step Navigation */}
              <motion.div 
                className="flex justify-center mb-12"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, ease: easing }}
                viewport={{ once: true }}
              >
                <div className="flex space-x-8">
                  {[1, 2, 3].map((step) => (
                    <motion.button
                      key={step}
                      onClick={() => setActiveStep(step)}
                      className={`px-6 py-3 rounded-lg font-semibold transition-all relative overflow-hidden ${
                        activeStep === step
                          ? 'bg-[#9CA3AF] text-white'
                          : 'bg-gray-800 text-gray-300'
                      }`}
                      whileHover={{
                        scale: 1.05,
                        y: -2,
                        transition: { type: "spring", stiffness: 400, damping: 10 }
                      }}
                      whileTap={{ scale: 0.95 }}
                      initial={{ opacity: 0, x: -20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      transition={{ delay: step * 0.1, duration: 0.6 }}
                      viewport={{ once: true }}
                    >
                      {activeStep === step && (
                        <motion.div
                          className="absolute inset-0 bg-[#9CA3AF]"
                          layoutId="activeStep"
                          transition={{ type: "spring", stiffness: 400, damping: 30 }}
                        />
                      )}
                      <span className="relative z-10">Step {step}</span>
                    </motion.button>
                  ))}
                </div>
              </motion.div>
              
              {/* Enhanced Step Content */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <motion.div 
                  className="space-y-6"
                  key={activeStep}
                  initial={{ opacity: 0, x: -50 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.6, ease: easing }}
                >
                  {activeStep === 1 && (
                    <>
                      <motion.h3 
                        className="text-3xl font-bold text-white"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2, duration: 0.6 }}
                      >
                        Choose Your Challenge
                      </motion.h3>
                      <motion.p 
                        className="text-gray-300 text-lg leading-relaxed"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3, duration: 0.6 }}
                      >
                        Select from our range of trading challenges based on your experience level and risk tolerance. 
                        From $10K to $100K accounts, all with no time limits.
                      </motion.p>
                      <motion.ul 
                        className="space-y-2 text-gray-400"
                        variants={staggerContainer}
                        initial="initial"
                        animate="animate"
                      >
                        {['Multiple account sizes available', 'Flexible profit targets', 'No time pressure'].map((item, index) => (
                          <motion.li 
                            key={index}
                            variants={staggerItem}
                            className="flex items-center"
                          >
                            <motion.div
                              className="w-2 h-2 bg-[#9CA3AF] rounded-full mr-3"
                              animate={{ scale: [1, 1.2, 1] }}
                              transition={{ duration: 2, repeat: Infinity, delay: index * 0.2 }}
                            />
                            {item}
                          </motion.li>
                        ))}
                      </motion.ul>
                    </>
                  )}
                  {/* Similar patterns for steps 2 and 3... */}
                  {activeStep === 2 && (
                    <>
                      <motion.h3 
                        className="text-3xl font-bold text-white"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2, duration: 0.6 }}
                      >
                        Trade & Prove Your Skills
                      </motion.h3>
                      <motion.p 
                        className="text-gray-300 text-lg leading-relaxed"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3, duration: 0.6 }}
                      >
                        Demonstrate your trading skills by reaching the profit target while staying within 
                        the maximum drawdown limits. Trade at your own pace with our advanced platform.
                      </motion.p>
                      <motion.ul 
                        className="space-y-2 text-gray-400"
                        variants={staggerContainer}
                        initial="initial"
                        animate="animate"
                      >
                        {['Real market conditions', 'Professional trading tools', 'Risk management focus'].map((item, index) => (
                          <motion.li 
                            key={index}
                            variants={staggerItem}
                            className="flex items-center"
                          >
                            <motion.div
                              className="w-2 h-2 bg-[#9CA3AF] rounded-full mr-3"
                              animate={{ scale: [1, 1.2, 1] }}
                              transition={{ duration: 2, repeat: Infinity, delay: index * 0.2 }}
                            />
                            {item}
                          </motion.li>
                        ))}
                      </motion.ul>
                    </>
                  )}
                  {activeStep === 3 && (
                    <>
                      <motion.h3 
                        className="text-3xl font-bold text-white"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2, duration: 0.6 }}
                      >
                        Get Funded & Keep 90%
                      </motion.h3>
                      <motion.p 
                        className="text-gray-300 text-lg leading-relaxed"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3, duration: 0.6 }}
                      >
                        Once you pass the evaluation, receive a funded account and keep up to 90% of your profits. 
                        Scale your account based on consistent performance.
                      </motion.p>
                      <motion.ul 
                        className="space-y-2 text-gray-400"
                        variants={staggerContainer}
                        initial="initial"
                        animate="animate"
                      >
                        {['Keep up to 90% of profits', 'Monthly payouts', 'Account scaling opportunities'].map((item, index) => (
                          <motion.li 
                            key={index}
                            variants={staggerItem}
                            className="flex items-center"
                          >
                            <motion.div
                              className="w-2 h-2 bg-[#9CA3AF] rounded-full mr-3"
                              animate={{ scale: [1, 1.2, 1] }}
                              transition={{ duration: 2, repeat: Infinity, delay: index * 0.2 }}
                            />
                            {item}
                          </motion.li>
                        ))}
                      </motion.ul>
                    </>
                  )}
                </motion.div>
                
                <motion.div 
                  className="flex justify-center"
                  key={`visual-${activeStep}`}
                  initial={{ opacity: 0, scale: 0.8, rotateY: 90 }}
                  animate={{ opacity: 1, scale: 1, rotateY: 0 }}
                  transition={{ duration: 0.8, ease: easing }}
                >
                  <div className="w-96 h-64 bg-gray-800/50 rounded-xl border border-gray-700 flex items-center justify-center relative overflow-hidden">
                    <motion.div
                      className="absolute inset-0 bg-gradient-to-r from-transparent via-[#9CA3AF]/10 to-transparent"
                      animate={{ x: [-300, 300] }}
                      transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                    />
                    <div className="text-gray-400 text-center relative z-10">
                      <motion.div 
                        className="w-16 h-16 bg-[#9CA3AF]/20 rounded-full flex items-center justify-center mx-auto mb-4"
                        animate={{ rotate: 360 }}
                        transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                      >
                        {activeStep === 1 && <DollarSign className="h-8 w-8 text-[#9CA3AF]" />}
                        {activeStep === 2 && <TrendingUp className="h-8 w-8 text-[#9CA3AF]" />}
                        {activeStep === 3 && <Award className="h-8 w-8 text-[#9CA3AF]" />}
                      </motion.div>
                      <p>Step {activeStep} Visualization</p>
                    </div>
                  </div>
                </motion.div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Enhanced Payouts & Certificates Section */}
      <section className="relative z-10 py-20 px-6">
        <div className="container mx-auto max-w-4xl">
          <motion.div 
            className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-center"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <motion.div 
              className="text-center lg:text-right"
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, ease: easing }}
              viewport={{ once: true }}
            >
              <h2 className="text-4xl font-bold text-white mb-4">Payouts</h2>
              <p className="text-gray-400">Real money, real results</p>
            </motion.div>
            
            <motion.div 
              className="flex justify-center"
              initial={{ opacity: 0, scale: 0.8, y: 50 }}
              whileInView={{ opacity: 1, scale: 1, y: 0 }}
              transition={{ 
                duration: 0.8, 
                delay: 0.2,
                type: "spring",
                stiffness: 200,
                damping: 15
              }}
              viewport={{ once: true }}
            >
              <div className="relative group">
                {/* Enhanced Wireframe Grid Background */}
                <motion.div 
                  className="absolute inset-0 opacity-30 transform rotate-45 scale-110"
                  animate={{ rotate: [45, 405] }}
                  transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                >
                  <div className="grid grid-cols-8 grid-rows-8 gap-1 w-full h-full">
                    {[...Array(64)].map((_, i) => (
                      <motion.div 
                        key={i} 
                        className="border border-[#9CA3AF]/20"
                        animate={{ opacity: [0.2, 0.5, 0.2] }}
                        transition={{ 
                          duration: 2, 
                          repeat: Infinity, 
                          delay: (i % 8) * 0.1 
                        }}
                      />
                    ))}
                  </div>
                </motion.div>
                
                {/* Enhanced Certificate Card */}
                <motion.div 
                  className="relative bg-gray-900/40 backdrop-blur-sm border border-gray-700/50 rounded-2xl p-8 transform group-hover:scale-105 transition-all duration-500 shadow-[0_0_50px_rgba(156,163,175,0.1)]"
                  whileHover={cardHover}
                  animate={{
                    y: [0, -5, 0],
                    boxShadow: [
                      "0 0 50px rgba(156, 163, 175, 0.1)",
                      "0 0 80px rgba(156, 163, 175, 0.2)",
                      "0 0 50px rgba(156, 163, 175, 0.1)"
                    ]
                  }}
                  transition={{
                    y: { duration: 4, repeat: Infinity, ease: "easeInOut" },
                    boxShadow: { duration: 3, repeat: Infinity, ease: "easeInOut" }
                  }}
                >
                  <div className="text-center space-y-4">
                    <motion.div 
                      className="w-16 h-16 bg-[#9CA3AF]/20 rounded-full flex items-center justify-center mx-auto"
                      animate={{ rotate: [0, 360] }}
                      transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                    >
                      <Award className="h-8 w-8 text-[#9CA3AF]" />
                    </motion.div>
                    <h3 className="text-xl font-bold text-white">Payout Certificate</h3>
                    <motion.div 
                      className="text-2xl font-bold text-[#9CA3AF]"
                      animate={{ scale: [1, 1.05, 1] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    >
                      $12,500
                    </motion.div>
                    <p className="text-gray-400 text-sm">Monthly Payout</p>
                    <div className="pt-4 border-t border-gray-700">
                      <p className="text-xs text-gray-500">Certified Trader Program</p>
                    </div>
                  </div>
                </motion.div>
              </div>
            </motion.div>
            
            <motion.div 
              className="text-center lg:text-left"
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, ease: easing, delay: 0.4 }}
              viewport={{ once: true }}
            >
              <h2 className="text-4xl font-bold text-white mb-4">Certificates</h2>
              <p className="text-gray-400">Verified achievements</p>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Enhanced Pricing Plans Section with Staggered Grid Animation */}
      <section className="relative z-10 py-20 px-6">
        <div className="container mx-auto max-w-7xl">
          <motion.h2 
            className="text-4xl md:text-5xl font-bold text-center text-white mb-16"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: easing }}
            viewport={{ once: true }}
          >
            Choose Your Challenge
          </motion.h2>
          
          <motion.div 
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true, amount: 0.1 }}
          >
            {pricingPlans.map((plan, index) => (
              <motion.div
                key={index}
                className={`relative group cursor-pointer ${
                  plan.popular ? 'lg:-mt-4' : ''
                }`}
                variants={staggerItem}
                whileHover={cardHover}
                transition={{ type: "spring", stiffness: 300, damping: 20 }}
              >
                {/* Enhanced Glassmorphism Card */}
                <div className={`relative bg-gray-900/40 backdrop-blur-sm border rounded-2xl p-6 h-full transition-all duration-500 overflow-hidden ${
                  plan.popular
                    ? 'border-[#9CA3AF] shadow-[0_0_30px_rgba(156,163,175,0.2)]'
                    : 'border-gray-700/50 group-hover:border-[#9CA3AF] group-hover:shadow-[0_0_30px_rgba(156,163,175,0.1)]'
                }`}>
                  {/* Animated Background Glow */}
                  <motion.div
                    className="absolute inset-0 bg-gradient-to-br from-[#9CA3AF]/5 to-transparent"
                    initial={{ opacity: 0, scale: 0.8 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.1 + 0.5, duration: 0.8 }}
                    viewport={{ once: true }}
                  />
                  
                  {/* Popular Badge */}
                  {plan.popular && (
                    <motion.div 
                      className="absolute -top-3 left-1/2 transform -translate-x-1/2"
                      initial={{ opacity: 0, y: -10, scale: 0.8 }}
                      whileInView={{ opacity: 1, y: 0, scale: 1 }}
                      transition={{ delay: index * 0.1 + 0.3, duration: 0.6 }}
                      viewport={{ once: true }}
                    >
                      <motion.div 
                        className="bg-[#9CA3AF] text-white px-4 py-1 rounded-full text-sm font-semibold"
                        animate={{ 
                          boxShadow: [
                            "0 0 10px rgba(156, 163, 175, 0.3)",
                            "0 0 20px rgba(156, 163, 175, 0.5)",
                            "0 0 10px rgba(156, 163, 175, 0.3)"
                          ]
                        }}
                        transition={{ duration: 2, repeat: Infinity }}
                      >
                        Most Popular
                      </motion.div>
                    </motion.div>
                  )}
                  
                  <div className="text-center space-y-6 relative z-10">
                    <motion.h3 
                      className="text-2xl font-bold text-white"
                      initial={{ opacity: 0, y: 20 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 + 0.2, duration: 0.6 }}
                      viewport={{ once: true }}
                    >
                      {plan.name}
                    </motion.h3>
                    
                    <motion.div
                      initial={{ opacity: 0, scale: 0.8 }}
                      whileInView={{ opacity: 1, scale: 1 }}
                      transition={{ delay: index * 0.1 + 0.3, duration: 0.6 }}
                      viewport={{ once: true }}
                    >
                      <span className="text-4xl font-bold text-[#9CA3AF]">{plan.price}</span>
                      <span className="text-gray-400 ml-2">{plan.period}</span>
                    </motion.div>
                    
                    <motion.ul 
                      className="space-y-3 text-left"
                      variants={staggerContainer}
                      initial="initial"
                      whileInView="animate"
                      viewport={{ once: true }}
                    >
                      {plan.features.map((feature, idx) => (
                        <motion.li 
                          key={idx} 
                          className="flex items-center text-gray-300"
                          variants={{
                            initial: { opacity: 0, x: -20 },
                            animate: { 
                              opacity: 1, 
                              x: 0,
                              transition: {
                                delay: index * 0.1 + idx * 0.05 + 0.4,
                                duration: 0.5
                              }
                            }
                          }}
                        >
                          <motion.div 
                            className="w-2 h-2 bg-[#9CA3AF] rounded-full mr-3"
                            animate={{ 
                              scale: [1, 1.2, 1],
                              opacity: [0.7, 1, 0.7]
                            }}
                            transition={{ 
                              duration: 2, 
                              repeat: Infinity, 
                              delay: idx * 0.2 
                            }}
                          />
                          {feature}
                        </motion.li>
                      ))}
                    </motion.ul>
                    
                    <motion.button 
                      className={`w-full py-3 rounded-lg font-semibold transition-all duration-300 relative overflow-hidden ${
                        plan.popular
                          ? 'bg-[#9CA3AF] text-white'
                          : 'bg-gray-800 text-white group-hover:bg-[#9CA3AF] group-hover:text-white'
                      }`}
                      initial={{ opacity: 0, y: 20 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 + 0.6, duration: 0.6 }}
                      viewport={{ once: true }}
                      whileHover={{
                        scale: 1.05,
                        transition: { type: "spring", stiffness: 400, damping: 10 }
                      }}
                      whileTap={{ scale: 0.95 }}
                    >
                      <motion.div
                        className="absolute inset-0 bg-gradient-to-r from-[#6B7280] to-[#9CA3AF]"
                        initial={{ x: "-100%" }}
                        whileHover={{ x: "100%" }}
                        transition={{ duration: 0.6 }}
                      />
                      <span className="relative z-10">Start Challenge</span>
                    </motion.button>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Enhanced Final CTA & Countdown Section */}
      <section className="relative z-10 py-20 px-6">
        <div className="container mx-auto max-w-4xl text-center">
          <motion.h2 
            className="text-3xl md:text-4xl font-bold text-white mb-6"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: easing }}
            viewport={{ once: true }}
          >
            Traders from more than 150 countries trust Fxology
          </motion.h2>
          <motion.p 
            className="text-gray-400 text-lg mb-12"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
          >
            Join thousands of successful traders who have already started their journey with us
          </motion.p>
          
          {/* Enhanced Countdown Timer */}
          <motion.div 
            className="mb-12"
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            viewport={{ once: true }}
          >
            <motion.p 
              className="text-[#9CA3AF] text-sm font-semibold mb-4"
              animate={{ opacity: [0.7, 1, 0.7] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              LIMITED TIME OFFER ENDS IN:
            </motion.p>
            <motion.div 
              className="flex justify-center space-x-8"
              variants={staggerContainer}
              initial="initial"
              whileInView="animate"
              viewport={{ once: true }}
            >
              {[
                { value: countdown.days, label: "DAYS" },
                { value: countdown.hours, label: "HOURS" },
                { value: countdown.minutes, label: "MINUTES" },
                { value: countdown.seconds, label: "SECONDS" }
              ].map((time, index) => (
                <motion.div 
                  key={time.label}
                  className="text-center"
                  variants={staggerItem}
                  whileHover={{ scale: 1.1, y: -5 }}
                >
                  <motion.div 
                    className="text-4xl md:text-5xl font-bold text-white mb-2"
                    animate={{ 
                      scale: time.label === "SECONDS" ? [1, 1.1, 1] : 1
                    }}
                    transition={{ 
                      duration: 1, 
                      repeat: time.label === "SECONDS" ? Infinity : 0 
                    }}
                  >
                    {time.value.toString().padStart(2, '0')}
                  </motion.div>
                  <div className="text-gray-400 text-sm">{time.label}</div>
                </motion.div>
              ))}
            </motion.div>
          </motion.div>
          
          {/* Enhanced Planet Arc with Shooting Stars */}
          <motion.div 
            className="relative mb-12"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            viewport={{ once: true }}
          >
            <svg className="w-full h-32 opacity-30" viewBox="0 0 400 100">
              <defs>
                <linearGradient id="arcGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#9CA3AF" stopOpacity="0" />
                  <stop offset="50%" stopColor="#9CA3AF" stopOpacity="0.8" />
                  <stop offset="100%" stopColor="#9CA3AF" stopOpacity="0" />
                </linearGradient>
              </defs>
              <motion.path
                d="M50,80 Q200,20 350,80"
                stroke="url(#arcGradient)"
                strokeWidth="2"
                fill="none"
                initial={{ pathLength: 0 }}
                whileInView={{ pathLength: 1 }}
                transition={{ duration: 2, ease: "easeInOut" }}
                viewport={{ once: true }}
              />
              {/* Enhanced Shooting Stars */}
              {[...Array(3)].map((_, i) => (
                <motion.circle 
                  key={i}
                  r={2 - i * 0.3} 
                  fill="#9CA3AF" 
                  opacity={0.8 - i * 0.2}
                  animate={{
                    x: [0, 400],
                    y: [60 + i * 5, 60 + i * 5]
                  }}
                  transition={{
                    duration: 3 + i,
                    repeat: Infinity,
                    delay: i * 1.5,
                    ease: "easeInOut"
                  }}
                />
              ))}
            </svg>
          </motion.div>
          
          <motion.button 
            className="bg-[#9CA3AF] text-white px-12 py-4 rounded-lg text-xl font-bold relative overflow-hidden shadow-[0_0_30px_rgba(156,163,175,0.3)]"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            whileHover={magneticHover}
            whileTap={{ scale: 0.95 }}
            animate={{
              boxShadow: [
                "0 0 30px rgba(156, 163, 175, 0.3)",
                "0 0 50px rgba(156, 163, 175, 0.5)",
                "0 0 30px rgba(156, 163, 175, 0.3)"
              ]
            }}
            transition={{
              opacity: { duration: 0.8, delay: 0.8 },
              y: { duration: 0.8, delay: 0.8 },
              boxShadow: { duration: 2, repeat: Infinity, ease: "easeInOut" }
            }}
          >
            <motion.div
              className="absolute inset-0 bg-gradient-to-r from-[#6B7280] to-[#9CA3AF]"
              initial={{ x: "-100%" }}
              whileHover={{ x: "100%" }}
              transition={{ duration: 0.8 }}
            />
            <span className="relative z-10">Start Your Challenge Now</span>
          </motion.button>
        </div>
      </section>

      {/* Enhanced FAQ Section with Smooth Accordion */}
      <section className="relative z-10 py-20 px-6">
        <div className="container mx-auto max-w-4xl">
          <motion.h2 
            className="text-4xl md:text-5xl font-bold text-center text-white mb-16"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: easing }}
            viewport={{ once: true }}
          >
            Frequently Asked Questions
          </motion.h2>
          
          <motion.div 
            className="space-y-4"
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true, amount: 0.1 }}
          >
            {faqData.map((faq, index) => (
              <motion.div 
                key={index} 
                className="bg-gray-900/40 backdrop-blur-sm border border-gray-700/50 rounded-xl overflow-hidden"
                variants={staggerItem}
                whileHover={{
                  borderColor: "rgba(156, 163, 175, 0.5)",
                  transition: { duration: 0.3 }
                }}
              >
                <motion.button
                  onClick={() => setOpenFaq(openFaq === index ? null : index)}
                  className="w-full px-6 py-6 text-left flex items-center justify-between hover:bg-gray-800/50 transition-colors"
                  whileHover={{ backgroundColor: "rgba(31, 41, 55, 0.5)" }}
                  whileTap={{ scale: 0.99 }}
                >
                  <span className="text-lg font-semibold text-white">{faq.question}</span>
                  <motion.div
                    animate={{ 
                      rotate: openFaq === index ? 45 : 0,
                      scale: openFaq === index ? 1.1 : 1
                    }}
                    transition={{ 
                      type: "spring", 
                      stiffness: 300, 
                      damping: 20 
                    }}
                  >
                    {openFaq === index ? (
                      <ChevronUp className="h-6 w-6 text-[#9CA3AF]" />
                    ) : (
                      <ChevronDown className="h-6 w-6 text-gray-400" />
                    )}
                  </motion.div>
                </motion.button>
                
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ 
                    height: openFaq === index ? "auto" : 0,
                    opacity: openFaq === index ? 1 : 0
                  }}
                  transition={{ 
                    duration: 0.4, 
                    ease: [0.25, 0.46, 0.45, 0.94]
                  }}
                  className="overflow-hidden"
                >
                  <motion.div 
                    className="px-6 pb-6"
                    initial={{ y: -10 }}
                    animate={{ y: openFaq === index ? 0 : -10 }}
                    transition={{ duration: 0.3, delay: openFaq === index ? 0.1 : 0 }}
                  >
                    <p className="text-gray-300 leading-relaxed">{faq.answer}</p>
                  </motion.div>
                </motion.div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Enhanced Who We Are Section with Flowing Line Graph */}
      <section className="relative z-10 py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <motion.div 
            className="text-center mb-16"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <motion.h2 
              className="text-5xl md:text-6xl font-bold text-white mb-8"
              initial={{ opacity: 0, y: 50, rotateX: 90 }}
              whileInView={{ opacity: 1, y: 0, rotateX: 0 }}
              transition={{ duration: 0.8, ease: easing }}
              viewport={{ once: true }}
            >
              {"Who we are?".split(" ").map((word, index) => (
                <motion.span
                  key={index}
                  initial={{ opacity: 0, y: 50 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{
                    duration: 0.6,
                    delay: index * 0.1,
                    ease: easing
                  }}
                  viewport={{ once: true }}
                  className="inline-block mr-4"
                >
                  {word}
                </motion.span>
              ))}
            </motion.h2>
            <motion.h3 
              className="text-3xl md:text-4xl font-bold text-[#9CA3AF]"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              viewport={{ once: true }}
            >
              {"And how it all started?".split(" ").map((word, index) => (
                <motion.span
                  key={index}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{
                    duration: 0.5,
                    delay: 0.5 + index * 0.05,
                    ease: easing
                  }}
                  viewport={{ once: true }}
                  className="inline-block mr-2"
                >
                  {word}
                </motion.span>
              ))}
            </motion.h3>
          </motion.div>
          
          {/* Enhanced Flowing Line Graph */}
          <motion.div 
            className="relative"
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            viewport={{ once: true }}
          >
            <svg className="w-full h-64 opacity-60" viewBox="0 0 800 200">
              <defs>
                <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#9CA3AF" stopOpacity="0.2" />
                  <stop offset="50%" stopColor="#9CA3AF" stopOpacity="1" />
                  <stop offset="100%" stopColor="#9CA3AF" stopOpacity="0.2" />
                </linearGradient>
              </defs>
              
              {/* Main Chart Line with Animation */}
              <motion.path
                d="M50,150 Q200,100 350,80 T750,60"
                stroke="url(#lineGradient)"
                strokeWidth="3"
                fill="none"
                initial={{ pathLength: 0, opacity: 0 }}
                whileInView={{ pathLength: 1, opacity: 1 }}
                transition={{ duration: 2, ease: "easeInOut" }}
                viewport={{ once: true }}
              />
              
              {/* Animated Data Points */}
              {[
                { cx: 200, cy: 100, delay: 1, value: "$2.5M" },
                { cx: 350, cy: 80, delay: 1.5, value: "$5.1M" },
                { cx: 500, cy: 75, delay: 2, value: "$8.7M" }
              ].map((point, index) => (
                <g key={index}>
                  <motion.circle 
                    cx={point.cx} 
                    cy={point.cy} 
                    r="4" 
                    fill="#9CA3AF" 
                    initial={{ scale: 0, opacity: 0 }}
                    whileInView={{ scale: 1, opacity: 0.8 }}
                    viewport={{ once: true }}
                    transition={{ 
                      delay: point.delay, 
                      duration: 0.6,
                      type: "spring",
                      stiffness: 400,
                      damping: 10
                    }}
                  />
                  
                  <motion.circle 
                    cx={point.cx} 
                    cy={point.cy} 
                    r="4" 
                    fill="#9CA3AF" 
                    animate={{ 
                      scale: [1, 1.3, 1],
                      opacity: [0.8, 1, 0.8]
                    }}
                    transition={{
                      scale: { duration: 2, repeat: Infinity, delay: index * 0.3 },
                      opacity: { duration: 2, repeat: Infinity, delay: index * 0.3 }
                    }}
                  />
                  
                  {/* Floating Numbers */}
                  <motion.text 
                    x={point.cx} 
                    y={point.cy - 15} 
                    fill="#9CA3AF" 
                    fontSize="12" 
                    textAnchor="middle" 
                    initial={{ opacity: 0, y: 10 }}
                    whileInView={{ opacity: 0.8, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ 
                      opacity: { delay: point.delay + 0.3, duration: 0.6 },
                      y: { delay: point.delay + 0.3, duration: 0.6 }
                    }}
                  >
                    {point.value}
                  </motion.text>
                </g>
              ))}
              
              {/* Background Grid Animation */}
              <defs>
                <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                  <motion.path 
                    d="M 40 0 L 0 0 0 40" 
                    fill="none" 
                    stroke="#9CA3AF" 
                    strokeWidth="0.5" 
                    opacity="0.1"
                    animate={{ opacity: [0.1, 0.3, 0.1] }}
                    transition={{ duration: 4, repeat: Infinity }}
                  />
                </pattern>
              </defs>
              <rect width="100%" height="100%" fill="url(#grid)" />
            </svg>
          </motion.div>
          
          <motion.div 
            className="max-w-3xl mx-auto text-center"
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true, amount: 0.3 }}
          >
            <motion.p 
              className="text-xl text-gray-300 leading-relaxed mb-8"
              variants={staggerItem}
            >
              Founded by professional traders with over 15 years of combined experience in the financial markets, 
              Fxology was created to democratize access to trading capital and provide opportunities for skilled 
              traders worldwide.
            </motion.p>
            <motion.p 
              className="text-lg text-gray-400"
              variants={staggerItem}
            >
              Our mission is to identify and fund talented traders while providing them with the tools, 
              support, and capital needed to succeed in today's dynamic financial markets.
            </motion.p>
          </motion.div>
        </div>
      </section>

      {/* Enhanced Footer with Staggered Animations */}
      <motion.footer 
        className="relative z-10 border-t border-gray-800/50 bg-gray-900/20 backdrop-blur-sm"
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: easing }}
        viewport={{ once: true }}
      >
        <div className="container mx-auto px-6 py-16">
          <motion.div 
            className="grid grid-cols-1 md:grid-cols-4 gap-8"
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true, amount: 0.1 }}
          >
            {/* Programs */}
            <motion.div variants={staggerItem}>
              <h4 className="text-lg font-semibold text-white mb-6">Programs</h4>
              <motion.ul 
                className="space-y-3"
                variants={staggerContainer}
                initial="initial"
                whileInView="animate"
                viewport={{ once: true }}
              >
                {['Trading Challenges', 'Funded Accounts', 'Educational Resources', 'Trading Platform'].map((item, index) => (
                  <motion.li 
                    key={item}
                    variants={staggerItem}
                  >
                    <motion.a 
                      href="#" 
                      className="text-gray-400 hover:text-[#9CA3AF] transition-colors"
                      whileHover={{ x: 5, transition: { duration: 0.2 } }}
                    >
                      {item}
                    </motion.a>
                  </motion.li>
                ))}
              </motion.ul>
            </motion.div>
            
            {/* About Us */}
            <motion.div variants={staggerItem}>
              <h4 className="text-lg font-semibold text-white mb-6">About Us</h4>
              <motion.ul 
                className="space-y-3"
                variants={staggerContainer}
                initial="initial"
                whileInView="animate"
                viewport={{ once: true }}
              >
                {['Our Story', 'Team', 'Careers', 'Contact'].map((item, index) => (
                  <motion.li 
                    key={item}
                    variants={staggerItem}
                  >
                    <motion.a 
                      href="#" 
                      className="text-gray-400 hover:text-[#9CA3AF] transition-colors"
                      whileHover={{ x: 5, transition: { duration: 0.2 } }}
                    >
                      {item}
                    </motion.a>
                  </motion.li>
                ))}
              </motion.ul>
            </motion.div>
            
            {/* Legal */}
            <motion.div variants={staggerItem}>
              <h4 className="text-lg font-semibold text-white mb-6">Legal</h4>
              <motion.ul 
                className="space-y-3"
                variants={staggerContainer}
                initial="initial"
                whileInView="animate"
                viewport={{ once: true }}
              >
                {['Terms of Service', 'Privacy Policy', 'Risk Disclosure', 'Compliance'].map((item, index) => (
                  <motion.li 
                    key={item}
                    variants={staggerItem}
                  >
                    <motion.a 
                      href="#" 
                      className="text-gray-400 hover:text-[#9CA3AF] transition-colors"
                      whileHover={{ x: 5, transition: { duration: 0.2 } }}
                    >
                      {item}
                    </motion.a>
                  </motion.li>
                ))}
              </motion.ul>
            </motion.div>
            
            {/* Social & Brand */}
            <motion.div variants={staggerItem}>
              <motion.div 
                className="flex items-center space-x-3 mb-6"
                whileHover={{ scale: 1.05 }}
                transition={{ type: "spring", stiffness: 400, damping: 10 }}
              >
                <motion.div
                  animate={{ rotate: [0, 360] }}
                  transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                >
                  <TrendingUp className="h-8 w-8 text-[#9CA3AF]" />
                </motion.div>
                <h4 className="text-2xl font-bold text-white">Fxology</h4>
              </motion.div>
              <motion.p 
                className="text-gray-400 mb-6"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3, duration: 0.6 }}
                viewport={{ once: true }}
              >
                Empowering traders worldwide with capital and opportunity.
              </motion.p>
              <motion.div 
                className="flex space-x-4"
                variants={staggerContainer}
                initial="initial"
                whileInView="animate"
                viewport={{ once: true }}
              >
                {[
                  { Icon: Users, delay: 0 },
                  { Icon: Globe, delay: 0.1 },
                  { Icon: Shield, delay: 0.2 }
                ].map(({ Icon, delay }, index) => (
                  <motion.a 
                    key={index}
                    href="#" 
                    className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-[#9CA3AF] hover:text-white transition-all"
                    variants={staggerItem}
                    whileHover={{
                      scale: 1.1,
                      rotate: 5,
                      transition: { type: "spring", stiffness: 400, damping: 10 }
                    }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <Icon className="h-5 w-5" />
                  </motion.a>
                ))}
              </motion.div>
            </motion.div>
          </motion.div>
          
          <motion.div 
            className="border-t border-gray-800 mt-12 pt-8 text-center"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.6 }}
            viewport={{ once: true }}
          >
            <p className="text-gray-500">© 2024 Fxology. All rights reserved. Trading involves risk of loss.</p>
          </motion.div>
        </div>
      </motion.footer>
    </div>
  )
}