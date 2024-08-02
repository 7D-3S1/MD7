// ==UserScript==
// @name         Gmail Sender Checker
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Check Gmail sender against backend API
// @author       You
// @match        https://mail.google.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Function to send email to backend for checking
    async function sendEmailToBackend(email) {
        const response = await fetch('http://127.0.0.1:5000/check_email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: email })
        });
        return response.json();
    }

    // Function to add status next to the sender email
    async function addStatusToSender() {
        // Get the sender email element
        const emailElement = document.querySelector('span[email]');
        if (emailElement) {
            const email = emailElement.getAttribute('email');
            const statusData = await sendEmailToBackend(email);
            if (statusData && statusData.data) {
                const score = statusData.data.score;
                const status = statusData.data.status;
                const statusText = `Score: ${score}, Status: ${status}`;
                
                // Create a new span element to display the status
                const statusSpan = document.createElement('span');
                statusSpan.textContent = statusText;
                statusSpan.style.color = status === 'valid' ? 'green' : 'red';
                statusSpan.style.marginLeft = '10px';
                
                // Append the status span next to the email element
                emailElement.parentNode.appendChild(statusSpan);
            }
        }
    }

    // Observe changes to the DOM to detect when an email is opened
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes) {
                for (let node of mutation.addedNodes) {
                    if (node.nodeType === 1) {
                        if (node.querySelector('span[email]')) {
                            addStatusToSender();
                        }
                    }
                }
            }
        });
    });

    // Start observing the DOM
    observer.observe(document.body, { childList: true, subtree: true });

})();
