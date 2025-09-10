import uuid
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

class InterfaceGenerator:
    """Service for generating user interfaces from natural language prompts"""
    
    # In-memory storage for demo purposes
    _interfaces: Dict[str, Dict] = {}
    
    @classmethod
    async def generate_from_prompt(cls, prompt: str) -> Dict[str, Any]:
        """Generate a complete interface from a natural language prompt"""
        interface_id = str(uuid.uuid4())
        
        # Simulate AI processing time
        await asyncio.sleep(2)
        
        # Mock interface generation based on prompt keywords
        if "customer support" in prompt.lower():
            interface = cls._generate_customer_support_interface()
        elif "dashboard" in prompt.lower():
            interface = cls._generate_dashboard_interface()
        elif "form" in prompt.lower():
            interface = cls._generate_form_interface()
        else:
            interface = cls._generate_generic_interface(prompt)
        
        interface["id"] = interface_id
        interface["prompt"] = prompt
        interface["created_at"] = datetime.utcnow().isoformat()
        
        cls._interfaces[interface_id] = interface
        return interface
    
    @classmethod
    async def get_interface(cls, interface_id: str) -> Optional[Dict[str, Any]]:
        """Get a previously generated interface"""
        return cls._interfaces.get(interface_id)
    
    @classmethod
    async def refine_interface(cls, interface_id: str, refinement_prompt: str) -> Dict[str, Any]:
        """Refine an existing interface with additional instructions"""
        interface = cls._interfaces.get(interface_id)
        if not interface:
            raise ValueError(f"Interface {interface_id} not found")
        
        # Simulate refinement processing
        await asyncio.sleep(1)
        
        # Mock refinement - in practice, this would use AI to modify the interface
        interface["html"] += f"\n<!-- Refined based on: {refinement_prompt} -->"
        interface["updated_at"] = datetime.utcnow().isoformat()
        interface["refinements"] = interface.get("refinements", []) + [refinement_prompt]
        
        return interface
    
    @classmethod
    async def generate_preview(cls, prompt: str) -> Dict[str, Any]:
        """Generate a quick preview without saving"""
        # Similar to generate_from_prompt but doesn't save to storage
        await asyncio.sleep(1)
        
        if "customer support" in prompt.lower():
            return cls._generate_customer_support_interface()
        elif "dashboard" in prompt.lower():
            return cls._generate_dashboard_interface()
        else:
            return cls._generate_generic_interface(prompt)
    
    @classmethod
    def _generate_customer_support_interface(cls) -> Dict[str, Any]:
        """Generate a customer support interface"""
        return {
            "html": """
            <div class="customer-support-dashboard">
                <header class="dashboard-header">
                    <h1>Customer Support Dashboard</h1>
                    <div class="status-indicators">
                        <span class="online">●</span> Online
                    </div>
                </header>
                <div class="main-content">
                    <div class="ticket-list">
                        <div class="ticket-item urgent">
                            <span class="ticket-id">#1234</span>
                            <span class="subject">Login issues with account verification</span>
                            <span class="priority">Urgent</span>
                        </div>
                        <div class="ticket-item normal">
                            <span class="ticket-id">#1233</span>
                            <span class="subject">Billing question resolved</span>
                            <span class="priority">Normal</span>
                        </div>
                    </div>
                    <div class="response-panel">
                        <h3>Draft Response</h3>
                        <textarea placeholder="AI-generated response will appear here..."></textarea>
                        <button class="send-button">Send & Close Ticket</button>
                    </div>
                </div>
            </div>
            """,
            "css": """
            .customer-support-dashboard {
                background: #0a0f1f;
                color: white;
                font-family: 'Inter', sans-serif;
                padding: 20px;
            }
            .dashboard-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                border-bottom: 1px solid #00BFFF;
                padding-bottom: 10px;
            }
            .main-content {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }
            .ticket-item {
                background: #1e293b;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #00BFFF;
                margin-bottom: 10px;
            }
            .ticket-item.urgent {
                border-left-color: #ef4444;
            }
            .response-panel textarea {
                width: 100%;
                height: 120px;
                background: #1e293b;
                border: 1px solid #00BFFF;
                color: white;
                padding: 10px;
                border-radius: 6px;
            }
            .send-button {
                background: linear-gradient(to right, #00BFFF, #8A2BE2);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                margin-top: 10px;
                cursor: pointer;
            }
            """,
            "javascript": """
            // Initialize customer support dashboard
            document.addEventListener('DOMContentLoaded', function() {
                const tickets = document.querySelectorAll('.ticket-item');
                const responsePanel = document.querySelector('.response-panel textarea');
                
                tickets.forEach(ticket => {
                    ticket.addEventListener('click', function() {
                        const ticketId = this.querySelector('.ticket-id').textContent;
                        const subject = this.querySelector('.subject').textContent;
                        responsePanel.value = `Responding to ${ticketId}: ${subject}...`;
                    });
                });
            });
            """,
            "components": {
                "TicketList": "Displays incoming support tickets",
                "ResponsePanel": "AI-powered response generator",
                "StatusIndicator": "Shows agent online status"
            }
        }
    
    @classmethod
    def _generate_dashboard_interface(cls) -> Dict[str, Any]:
        """Generate a generic dashboard interface"""
        return {
            "html": """
            <div class="dashboard">
                <nav class="sidebar">
                    <h2>Dashboard</h2>
                    <ul>
                        <li><a href="#overview">Overview</a></li>
                        <li><a href="#analytics">Analytics</a></li>
                        <li><a href="#settings">Settings</a></li>
                    </ul>
                </nav>
                <main class="main-content">
                    <div class="stats-grid">
                        <div class="stat-card">
                            <h3>Total Users</h3>
                            <p class="stat-number">1,234</p>
                        </div>
                        <div class="stat-card">
                            <h3>Active Sessions</h3>
                            <p class="stat-number">567</p>
                        </div>
                        <div class="stat-card">
                            <h3>Revenue</h3>
                            <p class="stat-number">$12,345</p>
                        </div>
                    </div>
                </main>
            </div>
            """,
            "css": """
            .dashboard {
                display: flex;
                min-height: 100vh;
                background: #0a0f1f;
                color: white;
                font-family: 'Inter', sans-serif;
            }
            .sidebar {
                width: 250px;
                background: #1e293b;
                padding: 20px;
                border-right: 1px solid #00BFFF;
            }
            .main-content {
                flex: 1;
                padding: 20px;
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
            }
            .stat-card {
                background: #1e293b;
                padding: 20px;
                border-radius: 8px;
                border: 1px solid #00BFFF;
            }
            .stat-number {
                font-size: 2rem;
                font-weight: bold;
                color: #00BFFF;
                margin: 10px 0;
            }
            """,
            "javascript": "// Dashboard initialization code",
            "components": {
                "Sidebar": "Navigation sidebar",
                "StatsGrid": "Statistics display grid",
                "StatCard": "Individual statistic cards"
            }
        }
    
    @classmethod
    def _generate_form_interface(cls) -> Dict[str, Any]:
        """Generate a form interface"""
        return {
            "html": """
            <form class="aether-form">
                <h2>Contact Form</h2>
                <div class="form-group">
                    <label for="name">Name</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="message">Message</label>
                    <textarea id="message" name="message" rows="4" required></textarea>
                </div>
                <button type="submit">Send Message</button>
            </form>
            """,
            "css": """
            .aether-form {
                max-width: 500px;
                margin: 0 auto;
                padding: 20px;
                background: #1e293b;
                border-radius: 8px;
                border: 1px solid #00BFFF;
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                color: white;
            }
            input, textarea {
                width: 100%;
                padding: 10px;
                background: #0a0f1f;
                border: 1px solid #00BFFF;
                color: white;
                border-radius: 4px;
            }
            button {
                background: linear-gradient(to right, #00BFFF, #8A2BE2);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                cursor: pointer;
            }
            """,
            "javascript": "// Form validation and submission code",
            "components": {
                "Form": "Contact form with validation",
                "FormGroup": "Form field containers"
            }
        }
    
    @classmethod
    def _generate_generic_interface(cls, prompt: str) -> Dict[str, Any]:
        """Generate a generic interface based on the prompt"""
        return {
            "html": f"""
            <div class="generated-interface">
                <h2>Generated Interface</h2>
                <p>This interface was generated from the prompt: "{prompt}"</p>
                <div class="content-area">
                    <p>Interface content would be dynamically generated here based on the specific requirements.</p>
                </div>
            </div>
            """,
            "css": """
            .generated-interface {
                padding: 20px;
                background: #1e293b;
                color: white;
                border-radius: 8px;
                border: 1px solid #00BFFF;
            }
            .content-area {
                margin-top: 20px;
                padding: 15px;
                background: #0a0f1f;
                border-radius: 6px;
            }
            """,
            "javascript": "// Generic interface functionality",
            "components": {
                "Interface": "Dynamically generated interface",
                "ContentArea": "Main content display area"
            }
        }