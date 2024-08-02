// ==UserScript==
// @name         Gmail Sender Checker
// @namespace    http://tampermonkey.net/
// @version      1.1
// @description  Check Gmail sender against backend API
// @author       You
// @match        https://mail.google.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Keep track of processed emails to avoid duplicate requests
    const processedEmails = new Set();

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
    async function addStatusToSender(emailElement) {
        if (!emailElement) return;

        const email = emailElement.getAttribute('email');
        console.log(email)
        if (processedEmails.has(email)) return; // Avoid duplicate requests

        const statusData = await sendEmailToBackend(email);
        if (statusData && statusData.data) {
            const score = statusData.data.score;
            const status = statusData.data.status;
            const statusText = `Score: ${score}, Status: ${status}`;

            // Create or update the status span element
            let statusSpan = emailElement.parentNode.querySelector('.status-span');
            if (!statusSpan) {
                statusSpan = document.createElement('span');
                statusSpan.className = 'status-span';
                statusSpan.style.marginLeft = '10px';
                emailElement.parentNode.appendChild(statusSpan);
            }

            statusSpan.textContent = statusText;
            statusSpan.style.color = status === 'valid' ? 'green' : 'red';

            processedEmails.add(email); // Mark email as processed
        }
    }

    // Observe changes to the DOM to detect when an email is opened
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes) {
                for (let node of mutation.addedNodes) {
                    if (node.nodeType === 1) {
                        const emailElement = node.querySelector('span[email]');
                        if (emailElement) {
                            addStatusToSender(emailElement);
                        }
                    }
                }
            }
        });
    });

    // Start observing the DOM
    observer.observe(document.body, { childList: true, subtree: true });

})();
