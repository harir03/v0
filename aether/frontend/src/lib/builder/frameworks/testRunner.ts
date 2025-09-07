#!/usr/bin/env node

/**
 * Test runner for Phase 3A Multi-Framework implementation
 * Run with: node testRunner.js
 */

import { MultiFrameworkTestSuite } from './testSuite'

async function runTests() {
  console.log('🚀 Starting Phase 3A Multi-Framework Test Suite...\n')
  
  try {
    const results = await MultiFrameworkTestSuite.runAllTests()
    const report = MultiFrameworkTestSuite.generateTestReport(results)
    
    console.log(report)
    
    const failedTests = results.filter(r => !r.success)
    if (failedTests.length > 0) {
      console.error('\n❌ Some tests failed!')
      process.exit(1)
    } else {
      console.log('\n✅ All tests passed!')
      process.exit(0)
    }
    
  } catch (error) {
    console.error('💥 Test suite failed to run:', error)
    process.exit(1)
  }
}

// Run tests if this file is executed directly
if (require.main === module) {
  runTests()
}

export { runTests }