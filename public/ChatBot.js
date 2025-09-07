//// Medical Chatbot functionality
//class MedicalChatbot {
//    constructor() {
//        this.initializeBot();
//        this.setupEventListeners();
//        this.medicalKnowledge = this.getMedicalKnowledge();
//    }
//
//    initializeBot() {
//        // Create chatbot UI elements
//        this.createChatbotUI();
//
//        // Add welcome message
//        this.addBotMessage("Hello! I'm MedAssistant, your AI health assistant. I can provide general medical information, explain health terms, and offer wellness suggestions. How can I help you today?");
//    }
//
//    createChatbotUI() {
//        // This would be handled by the HTML structure
//        // Just ensuring the messages container exists
//        this.messagesContainer = document.getElementById('medicalChatMessages');
//        if (!this.messagesContainer) {
//            console.error('Medical chat messages container not found');
//        }
//    }
//
//    setupEventListeners() {
//        // Send message on button click
//        const sendButton = document.getElementById('sendMedicalMessageBtn');
//        if (sendButton) {
//            sendButton.addEventListener('click', () => this.handleUserMessage());
//        }
//
//        // Send message on Enter key
//        const inputField = document.getElementById('medicalChatInput');
//        if (inputField) {
//            inputField.addEventListener('keypress', (e) => {
//                if (e.key === 'Enter') {
//                    this.handleUserMessage();
//                }
//            });
//        }
//    }
//
//    handleUserMessage() {
//        const inputField = document.getElementById('medicalChatInput');
//        if (!inputField) return;
//
//        const userMessage = inputField.value.trim();
//        if (userMessage === '') return;
//
//        // Add user message to chat
//        this.addUserMessage(userMessage);
//
//        // Clear input field
//        inputField.value = '';
//
//        // Process and respond to message
//        setTimeout(() => {
//            this.processMessage(userMessage);
//        }, 500);
//    }
//
//    addUserMessage(message) {
//        this.addMessage(message, 'user');
//    }
//
//    addBotMessage(message) {
//        this.addMessage(message, 'bot');
//    }
//
//    addMessage(message, sender) {
//        if (!this.messagesContainer) return;
//
//        const messageDiv = document.createElement('div');
//        messageDiv.classList.add('medical-message');
//        messageDiv.classList.add(sender === 'bot' ? 'bot-message' : 'user-message');
//
//        const now = new Date();
//        const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
//
//        messageDiv.innerHTML = `
//            <p>${message}</p>
//            <div class="message-time">${time}</div>
//        `;
//
//        this.messagesContainer.appendChild(messageDiv);
//        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
//    }
//
//    processMessage(userMessage) {
//        const lowerCaseMessage = userMessage.toLowerCase();
//        let response = "I understand your concern. Can you tell me more about that?";
//
//        // Check for emergency keywords first
//        if (this.isEmergencyMessage(lowerCaseMessage)) {
//            response = "🚨 If this is a medical emergency, please call your local emergency number immediately! Do not rely on AI assistance for emergency situations.";
//            this.addBotMessage(response);
//            return;
//        }
//
//        // Check for specific medical topics
//        for (const [keyword, responses] of Object.entries(this.medicalKnowledge)) {
//            if (lowerCaseMessage.includes(keyword)) {
//                response = responses[Math.floor(Math.random() * responses.length)];
//                break;
//            }
//        }
//
//        // Add slight delay to simulate processing
//        setTimeout(() => {
//            this.addBotMessage(response);
//        }, 800 + Math.random() * 700);
//    }
//
//    isEmergencyMessage(message) {
//        const emergencyKeywords = [
//            'emergency', '911', 'urgent', 'dying', 'heart attack', 'stroke',
//            'chest pain', 'bleeding', 'unconscious', 'can\'t breathe', 'choking'
//        ];
//
//        return emergencyKeywords.some(keyword => message.includes(keyword));
//    }
//
//    getMedicalKnowledge() {
//        return {
//            'symptom': [
//                "Symptoms can vary widely depending on the condition. It's important to track when your symptoms started, what makes them better or worse, and any other details that might help a healthcare provider understand what's happening.",
//                "I can provide general information about symptoms, but remember that only a healthcare professional can properly diagnose medical conditions based on symptoms."
//            ],
//            'pain': [
//                "Pain is your body's way of signaling that something might be wrong. The location, type, and duration of pain can help identify its cause.",
//                "For persistent or severe pain, it's important to consult with a healthcare provider to determine the cause and appropriate treatment."
//            ],
//            'headache': [
//                "Headaches can have many causes including tension, dehydration, or more serious conditions. Most headaches are not serious, but if you have a sudden severe headache or one accompanied by other symptoms like vision changes, it's important to seek medical attention.",
//                "Staying hydrated, managing stress, and maintaining good posture can help prevent some types of headaches."
//            ],
//            'fever': [
//                "A fever is usually a sign that your body is fighting an infection. Most fevers aren't dangerous, but very high fevers or fevers in infants require medical attention.",
//                "Stay hydrated and rest if you have a fever. Contact a doctor if your fever is very high, doesn't improve with medication, or lasts more than a few days."
//            ],
//            'blood pressure': [
//                "Blood pressure measures the force of blood against your artery walls. Normal blood pressure is typically around 120/80 mmHg.",
//                "Lifestyle changes like reducing salt intake, regular exercise, and maintaining a healthy weight can help manage blood pressure."
//            ],
//            'diabetes': [
//                "Diabetes is a condition where the body has trouble regulating blood sugar. There are different types with different management approaches.",
//                "Managing diabetes typically involves monitoring blood sugar, medication if prescribed, healthy eating, and regular physical activity."
//            ],
//            'exercise': [
//                "Regular exercise has many health benefits including improved cardiovascular health, better mood, and weight management.",
//                "Most adults should aim for at least 150 minutes of moderate-intensity exercise per week, but it's important to start slowly if you're new to exercise."
//            ],
//            'diet': [
//                "A balanced diet with plenty of fruits, vegetables, whole grains, and lean proteins supports overall health.",
//                "The Mediterranean diet is often recommended for its heart health benefits, but the best diet is one that you can maintain long-term and meets your nutritional needs."
//            ],
//            'medication': [
//                "It's important to take medications as prescribed by your healthcare provider and to be aware of potential side effects.",
//                "Never stop taking prescription medication without consulting your doctor, even if you're feeling better."
//            ],
//            'sleep': [
//                "Most adults need 7-9 hours of sleep per night for optimal health. Poor sleep can affect both physical and mental health.",
//                "Good sleep hygiene includes maintaining a consistent sleep schedule, creating a restful environment, and avoiding screens before bedtime."
//            ],
//            'stress': [
//                "Some stress is normal, but chronic stress can negatively impact your health. Finding healthy coping mechanisms is important.",
//                "Techniques like deep breathing, meditation, and regular physical activity can help manage stress levels."
//            ]
//        };
//    }
//}
//
//// Initialize the chatbot when the page loads
//document.addEventListener('DOMContentLoaded', function() {
//    // Only initialize if we're on the chatbot tab or page
//    const chatbotTab = document.getElementById('chatbot');
//    if (chatbotTab) {
//        new MedicalChatbot();
//    }
//});


// === Patient Info ===
const patientData = {
  name: "Sarah Johnson",
  email: "sarah.j@example.com",
  profileImage: "https://xsgames.co/randomusers/avatar.php?g=female&id=pat1"
};

// === Doctors List ===
const doctors = [
  { id: 1, name: "Dr. Michael Chen", specialty: "Cardiology", availability: "Available now", img: "https://xsgames.co/randomusers/avatar.php?g=male&id=doc1" },
  { id: 2, name: "Dr. Emily Rodriguez", specialty: "Endocrinology", availability: "Available in 1 hour", img: "https://xsgames.co/randomusers/avatar.php?g=female&id=doc2" },
  { id: 3, name: "Dr. James Wilson", specialty: "Orthopedics", availability: "Available tomorrow", img: "https://xsgames.co/randomusers/avatar.php?g=male&id=doc3" }
];

let currentDoctor = doctors[0];

// === Load Patient ===
function loadPatientDetails() {
  document.getElementById('usernameDisplay').textContent = `Welcome, ${patientData.name.split(' ')[0]}!`;
}

// === Doctor Modal ===
function setupDoctorModal() {
  const doctorModal = document.getElementById('doctorModal');
  const doctorSelector = document.getElementById('doctorSelector');
  const closeModalBtn = document.getElementById('closeModalBtn');
  const doctorList = document.getElementById('doctorList');

  doctors.forEach(doctor => {
    const item = document.createElement('div');
    item.classList.add('doctor-item');
    item.innerHTML = `
      <img src="${doctor.img}" class="doctor-img">
      <div><h4>${doctor.name}</h4><p>${doctor.specialty}</p></div>
      <span class="doctor-availability">${doctor.availability}</span>
    `;
    item.addEventListener('click', () => {
      currentDoctor = doctor;
      updateDoctorSelector();
      doctorModal.style.display = 'none';
      showAlert(`Now chatting with ${doctor.name}`, 'success');
      addMessage(`Hello ${patientData.name.split(' ')[0]}! I'm ${doctor.name}. How can I help you today?`, 'doctor');
    });
    doctorList.appendChild(item);
  });

  doctorSelector.addEventListener('click', () => doctorModal.style.display = 'flex');
  closeModalBtn.addEventListener('click', () => doctorModal.style.display = 'none');
  window.addEventListener('click', e => { if (e.target === doctorModal) doctorModal.style.display = 'none'; });
}

function updateDoctorSelector() {
  const doctorSelector = document.getElementById('doctorSelector');
  doctorSelector.innerHTML = `
    <img src="${currentDoctor.img}" class="doctor-img">
    <div><h3>${currentDoctor.name}</h3><p>${currentDoctor.specialty}</p></div>
    <i class="fas fa-chevron-down"></i>
  `;
  doctorSelector.addEventListener('click', () => document.getElementById('doctorModal').style.display = 'flex');
}

// === Chat System ===
function addMessage(text, sender) {
  const messagesContainer = document.getElementById('chatMessages');
  const msg = document.createElement('div');
  msg.classList.add('message', sender === 'doctor' ? 'doctor-message' : 'patient-message');

  const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  msg.innerHTML = `<p>${text}</p><div class="message-time">${time}</div>`;
  messagesContainer.appendChild(msg);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function setupChat() {
  const input = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendMessageBtn');

  function processMessage(message) {
    setTimeout(() => {
      let response = "Can you tell me more about your symptoms?";
      if (message.toLowerCase().includes('pain')) response = "Sorry to hear that. Where is the pain located?";
      if (message.toLowerCase().includes('appointment')) response = "I can help schedule an appointment. Which day works for you?";
      if (message.toLowerCase().includes('thank')) response = "You're welcome! Is there anything else?";
      addMessage(response, 'doctor');
    }, 1000);
  }

  sendBtn.addEventListener('click', () => {
    const msg = input.value.trim();
    if (msg) {
      addMessage(msg, 'patient');
      input.value = '';
      processMessage(msg);
    }
  });

  input.addEventListener('keypress', e => { if (e.key === 'Enter') sendBtn.click(); });
}

// === Alerts ===
function showAlert(message, type = 'info') {
  const alertContainer = document.getElementById('alertContainer');
  const alert = document.createElement('div');
  alert.classList.add('alert', type);
  alert.innerHTML = `<i class="fas fa-info-circle"></i><div>${message}</div>`;
  alertContainer.appendChild(alert);
  setTimeout(() => {
    alert.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => alert.remove(), 300);
  }, 4000);
}

// === Buttons ===
function setupButtons() {
  document.getElementById('logoutBtn').addEventListener('click', () => showAlert("Logged out", "warning"));
  document.getElementById('notificationsBtn').addEventListener('click', () => showAlert("You have 3 notifications", "info"));
  document.querySelector('.btn-success').addEventListener('click', () => showAlert(`Starting video call with ${currentDoctor.name}`, "success"));
}

// === Init ===
document.addEventListener('DOMContentLoaded', () => {
  loadPatientDetails();
  setupDoctorModal();
  setupChat();
  setupButtons();
  showAlert("Welcome back! You have 3 new notifications.", "info");
});
