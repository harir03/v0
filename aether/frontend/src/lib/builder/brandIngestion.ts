import { ThemeSpec } from '@/types/builder'

/**
 * Brand Ingestion System
 * Extracts design tokens from logos, screenshots, and brand assets
 */
export class BrandIngestionService {
  /**
   * Extract brand colors from uploaded image
   */
  async extractColorsFromImage(imageFile: File): Promise<BrandColors> {
    return new Promise((resolve) => {
      const canvas = document.createElement('canvas')
      const ctx = canvas.getContext('2d')!
      const img = new Image()
      
      img.onload = () => {
        canvas.width = img.width
        canvas.height = img.height
        ctx.drawImage(img, 0, 0)
        
        const colors = this.analyzeImageColors(ctx, canvas.width, canvas.height)
        resolve(colors)
      }
      
      img.src = URL.createObjectURL(imageFile)
    })
  }

  /**
   * Analyze image to extract dominant colors
   */
  private analyzeImageColors(ctx: CanvasRenderingContext2D, width: number, height: number): BrandColors {
    const imageData = ctx.getImageData(0, 0, width, height)
    const data = imageData.data
    const colorMap = new Map<string, number>()
    
    // Sample pixels (every 10th pixel for performance)
    for (let i = 0; i < data.length; i += 40) {
      const r = data[i]
      const g = data[i + 1]
      const b = data[i + 2]
      const alpha = data[i + 3]
      
      // Skip transparent pixels
      if (alpha < 128) continue
      
      // Quantize colors to reduce noise
      const quantizedR = Math.round(r / 32) * 32
      const quantizedG = Math.round(g / 32) * 32
      const quantizedB = Math.round(b / 32) * 32
      
      const colorKey = `${quantizedR},${quantizedG},${quantizedB}`
      colorMap.set(colorKey, (colorMap.get(colorKey) || 0) + 1)
    }
    
    // Get most frequent colors
    const sortedColors = Array.from(colorMap.entries())
      .sort(([, a], [, b]) => b - a)
      .slice(0, 10)
      .map(([color]) => {
        const [r, g, b] = color.split(',').map(Number)
        return this.rgbToHex(r, g, b)
      })
    
    return this.generateBrandPalette(sortedColors)
  }

  /**
   * Generate comprehensive brand palette from dominant colors
   */
  private generateBrandPalette(dominantColors: string[]): BrandColors {
    const primary = dominantColors[0] || '#3b82f6'
    const secondary = dominantColors[1] || '#6366f1'
    const accent = dominantColors[2] || '#f59e0b'
    
    return {
      primary: {
        50: this.lightenColor(primary, 0.95),
        100: this.lightenColor(primary, 0.9),
        200: this.lightenColor(primary, 0.8),
        300: this.lightenColor(primary, 0.6),
        400: this.lightenColor(primary, 0.4),
        500: primary,
        600: this.darkenColor(primary, 0.1),
        700: this.darkenColor(primary, 0.2),
        800: this.darkenColor(primary, 0.3),
        900: this.darkenColor(primary, 0.4),
      },
      secondary: {
        50: this.lightenColor(secondary, 0.95),
        100: this.lightenColor(secondary, 0.9),
        200: this.lightenColor(secondary, 0.8),
        300: this.lightenColor(secondary, 0.6),
        400: this.lightenColor(secondary, 0.4),
        500: secondary,
        600: this.darkenColor(secondary, 0.1),
        700: this.darkenColor(secondary, 0.2),
        800: this.darkenColor(secondary, 0.3),
        900: this.darkenColor(secondary, 0.4),
      },
      accent: {
        50: this.lightenColor(accent, 0.95),
        100: this.lightenColor(accent, 0.9),
        200: this.lightenColor(accent, 0.8),
        300: this.lightenColor(accent, 0.6),
        400: this.lightenColor(accent, 0.4),
        500: accent,
        600: this.darkenColor(accent, 0.1),
        700: this.darkenColor(accent, 0.2),
        800: this.darkenColor(accent, 0.3),
        900: this.darkenColor(accent, 0.4),
      },
      neutral: {
        50: '#f9fafb',
        100: '#f3f4f6',
        200: '#e5e7eb',
        300: '#d1d5db',
        400: '#9ca3af',
        500: '#6b7280',
        600: '#4b5563',
        700: '#374151',
        800: '#1f2937',
        900: '#111827',
      }
    }
  }

  /**
   * Extract typography preferences from brand analysis
   */
  async extractTypography(imageFile?: File, brandName?: string): Promise<TypographyProfile> {
    // Analyze brand characteristics to suggest fonts
    const brandCharacter = this.analyzeBrandCharacter(brandName)
    
    return {
      headings: this.selectHeadingFont(brandCharacter),
      body: this.selectBodyFont(brandCharacter),
      scale: this.generateTypeScale(),
      weights: ['300', '400', '500', '600', '700'],
      spacing: {
        letterSpacing: brandCharacter.modern ? '-0.025em' : '0',
        lineHeight: brandCharacter.readable ? '1.6' : '1.5'
      }
    }
  }

  /**
   * Convert brand analysis to theme specification
   */
  async generateThemeFromBrand(brandAssets: BrandAssets): Promise<ThemeSpec> {
    let colors: BrandColors | undefined
    let typography: TypographyProfile | undefined
    
    if (brandAssets.logo) {
      colors = await this.extractColorsFromImage(brandAssets.logo)
    }
    
    if (brandAssets.logo || brandAssets.brandName) {
      typography = await this.extractTypography(brandAssets.logo, brandAssets.brandName)
    }
    
    return {
      primaryColor: colors?.primary[500] || '#3b82f6',
      secondaryColor: colors?.secondary[500] || '#6366f1',
      accentColor: colors?.accent[500] || '#f59e0b',
      backgroundColor: '#ffffff',
      textColor: colors?.neutral[900] || '#111827',
      fontFamily: typography?.headings || 'Inter',
      spacing: {
        xs: '0.5rem',
        sm: '1rem',
        md: '1.5rem',
        lg: '2rem',
        xl: '3rem'
      },
      borderRadius: brandAssets.style === 'modern' ? '0.75rem' : '0.375rem',
      shadows: brandAssets.style === 'premium' ? 'enhanced' : 'subtle'
    }
  }

  // Helper methods
  private rgbToHex(r: number, g: number, b: number): string {
    return '#' + [r, g, b].map(x => x.toString(16).padStart(2, '0')).join('')
  }

  private lightenColor(hex: string, amount: number): string {
    const num = parseInt(hex.replace('#', ''), 16)
    const r = Math.min(255, Math.floor((num >> 16) + (255 - (num >> 16)) * amount))
    const g = Math.min(255, Math.floor(((num >> 8) & 0x00FF) + (255 - ((num >> 8) & 0x00FF)) * amount))
    const b = Math.min(255, Math.floor((num & 0x0000FF) + (255 - (num & 0x0000FF)) * amount))
    return `#${((r << 16) | (g << 8) | b).toString(16).padStart(6, '0')}`
  }

  private darkenColor(hex: string, amount: number): string {
    const num = parseInt(hex.replace('#', ''), 16)
    const r = Math.max(0, Math.floor((num >> 16) * (1 - amount)))
    const g = Math.max(0, Math.floor(((num >> 8) & 0x00FF) * (1 - amount)))
    const b = Math.max(0, Math.floor((num & 0x0000FF) * (1 - amount)))
    return `#${((r << 16) | (g << 8) | b).toString(16).padStart(6, '0')}`
  }

  private analyzeBrandCharacter(brandName?: string): BrandCharacter {
    // Simple heuristics for brand character analysis
    const name = brandName?.toLowerCase() || ''
    
    return {
      modern: name.includes('tech') || name.includes('ai') || name.includes('digital'),
      premium: name.includes('luxury') || name.includes('premium') || name.includes('elite'),
      playful: name.includes('fun') || name.includes('play') || name.includes('joy'),
      readable: true,
      professional: !name.includes('fun') && !name.includes('play')
    }
  }

  private selectHeadingFont(character: BrandCharacter): string {
    if (character.modern) return 'Inter'
    if (character.premium) return 'Playfair Display'
    if (character.playful) return 'Nunito'
    return 'Inter'
  }

  private selectBodyFont(character: BrandCharacter): string {
    if (character.readable) return 'Inter'
    if (character.premium) return 'Source Serif Pro'
    return 'Inter'
  }

  private generateTypeScale(): TypeScale {
    return {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
      '4xl': '2.25rem',
      '5xl': '3rem',
      '6xl': '3.75rem'
    }
  }
}

// Type definitions
export interface BrandColors {
  primary: ColorScale
  secondary: ColorScale
  accent: ColorScale
  neutral: ColorScale
}

export interface ColorScale {
  50: string
  100: string
  200: string
  300: string
  400: string
  500: string
  600: string
  700: string
  800: string
  900: string
}

export interface TypographyProfile {
  headings: string
  body: string
  scale: TypeScale
  weights: string[]
  spacing: {
    letterSpacing: string
    lineHeight: string
  }
}

export interface TypeScale {
  xs: string
  sm: string
  base: string
  lg: string
  xl: string
  '2xl': string
  '3xl': string
  '4xl': string
  '5xl': string
  '6xl': string
}

export interface BrandAssets {
  logo?: File
  screenshot?: File
  brandName?: string
  industry?: string
  style?: 'modern' | 'classic' | 'premium' | 'playful'
  colors?: string[]
}

interface BrandCharacter {
  modern: boolean
  premium: boolean
  playful: boolean
  readable: boolean
  professional: boolean
}