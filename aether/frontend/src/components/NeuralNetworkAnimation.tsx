'use client'

import { useEffect, useRef } from 'react'

export default function NeuralNetworkAnimation() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    // Neural network nodes
    const nodes: Array<{
      x: number
      y: number
      vx: number
      vy: number
      radius: number
      connections: number[]
    }> = []

    // Create nodes
    const nodeCount = 50
    for (let i = 0; i < nodeCount; i++) {
      nodes.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        radius: Math.random() * 3 + 1,
        connections: [],
      })
    }

    // Mouse position for interaction
    let mouseX = 0
    let mouseY = 0
    
    const handleMouseMove = (e: MouseEvent) => {
      mouseX = e.clientX
      mouseY = e.clientY
    }
    window.addEventListener('mousemove', handleMouseMove)

    // Animation loop
    const animate = () => {
      ctx.fillStyle = 'rgba(0, 8, 20, 0.05)'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      // Update and draw nodes
      nodes.forEach((node, i) => {
        // Update position
        node.x += node.vx
        node.y += node.vy

        // Bounce off edges
        if (node.x < 0 || node.x > canvas.width) node.vx *= -1
        if (node.y < 0 || node.y > canvas.height) node.vy *= -1

        // Mouse interaction
        const mouseDistance = Math.sqrt((mouseX - node.x) ** 2 + (mouseY - node.y) ** 2)
        if (mouseDistance < 100) {
          const angle = Math.atan2(mouseY - node.y, mouseX - node.x)
          node.vx += Math.cos(angle) * 0.01
          node.vy += Math.sin(angle) * 0.01
        }

        // Draw connections
        node.connections = []
        nodes.forEach((otherNode, j) => {
          if (i !== j) {
            const distance = Math.sqrt((node.x - otherNode.x) ** 2 + (node.y - otherNode.y) ** 2)
            if (distance < 120) {
              node.connections.push(j)
              
              // Draw connection line with gradient colors
              const opacity = (120 - distance) / 120
              const colors = ['#00d9ff', '#6366f1', '#ec4899']
              const colorIndex = Math.floor((distance / 120) * colors.length)
              const color = colors[colorIndex] || colors[0]
              
              ctx.strokeStyle = `${color}${Math.floor(opacity * 80).toString(16).padStart(2, '0')}`
              ctx.lineWidth = 0.8
              ctx.beginPath()
              ctx.moveTo(node.x, node.y)
              ctx.lineTo(otherNode.x, otherNode.y)
              ctx.stroke()
            }
          }
        })

        // Draw node with enhanced gradient
        const gradient = ctx.createRadialGradient(node.x, node.y, 0, node.x, node.y, node.radius * 3)
        gradient.addColorStop(0, '#00d9ff')
        gradient.addColorStop(0.5, '#6366f1')
        gradient.addColorStop(1, 'rgba(0, 217, 255, 0)')
        
        ctx.fillStyle = gradient
        ctx.beginPath()
        ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2)
        ctx.fill()

        // Add enhanced glow effect
        const glowColors = ['#00d9ff', '#6366f1', '#ec4899']
        const time = Date.now() * 0.001
        const colorIndex = Math.floor((Math.sin(time + i * 0.1) + 1) * 1.5) % glowColors.length
        
        ctx.shadowColor = glowColors[colorIndex]
        ctx.shadowBlur = 15 + Math.sin(time + i * 0.1) * 5
        ctx.fillStyle = glowColors[colorIndex]
        ctx.beginPath()
        ctx.arc(node.x, node.y, node.radius * 0.6, 0, Math.PI * 2)
        ctx.fill()
        ctx.shadowBlur = 0
      })

      requestAnimationFrame(animate)
    }

    animate()

    return () => {
      window.removeEventListener('resize', resizeCanvas)
      window.removeEventListener('mousemove', handleMouseMove)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 w-full h-full opacity-60"
      style={{ pointerEvents: 'none' }}
    />
  )
}