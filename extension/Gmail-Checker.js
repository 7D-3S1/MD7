// ==UserScript==
// @name         Gmail Sender Checker
// @namespace    http://tampermonkey.net/
// @version      1.2
// @description  Check Gmail sender against backend API and handle text selection
// @author       iach526
// @match        https://mail.google.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Keep track of processed emails to avoid duplicate requests
    const processedEmails = new Set();
    let linksProcessed = new WeakSet(); //超連結標籤集合

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
        console.log(email);
        if (processedEmails.has(email)) return; // Avoid duplicate requests
        
        const statusData = await sendEmailToBackend(email);
        if (statusData && statusData.data) {
            console.log("type of status",statusData.data,"\n",typeof(statusData.data));
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
    async function postUrlCheck(href) {
        const response = await fetch('http://127.0.0.1:5000/url_check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: href })
        });
        return response.json();
    }
    async function handleHref(href) {
        const response=await postUrlCheck(href);
        const malicious=response.data.attributes.stats.malicious//惡意程度
        const msg=`
            預估網址惡意程度：${malicious}\n
            確定要打開這個鏈接嗎？\n
            ${href}
        `
        if (confirm(msg)) {
            // 用戶確認，繼續打開鏈接
            window.open(href, '_blank');
        } 
        // else {
        //     // 用戶取消，不執行任何操作
        //     console.log("用戶取消了鏈接打開。");
        // }
        return
    }



    // Observe changes to the DOM to detect when an email is opened
    const observer = new MutationObserver((mutations) => {
        const url = window.location.href;
        var pre=undefined//上一次的捕捉結果
        const regex = /^https:\/\/mail\.google\.com\/mail\/u\/0\/#(.+?)\/(.+)$/; // 正則表達式匹配 /u/0/# 后面有参数的 URL
        if (regex.test(url)) {
            mutations.forEach((mutation) => {
                if (mutation.addedNodes) {
                    for (let node of mutation.addedNodes) {
                        if (node.nodeType === 1) {
                            const emailElement = node.querySelector('span[email]');
                            if (emailElement && pre!=emailElement) {
                                addStatusToSender(emailElement);
                                console.log("查看一封信，檢查 mail:",emailElement)
                                pre=emailElement
                                break;
                            }
                        }
                    }
                }
            });
            const links = document.querySelectorAll('a');
            links.forEach(link => {
                if (!linksProcessed.has(link)) { 
                    linksProcessed.add(link);
                    link.addEventListener('click', function(event) {
                        event.preventDefault(); // 防止默認的連結跳轉行為
                        console.log("line start！");
                        handleHref(link.href); // 
                    });
                }
            });
        }
        else
        {
            pre=undefined//離開郵件頁面到收件匣，重置狀態
            linksProcessed = new WeakSet(); // 重置超連結集合
        }

    });

    // Start observing the DOM
    observer.observe(document.body, { childList: true, subtree: true });

    // //選取文字跳出小幫手 icon
    function TextSelectionHelper() {
        document.addEventListener('mouseup', (event) => {
            const selection = window.getSelection();
            const selectedText = selection.toString().trim();
            const icon = document.getElementById('custom-icon');
            //被選取後在鼠標旁邊彈出送 去解析 的 icon
            if (selectedText.length > 0) {
                showCustomIcon(selection, event.pageX, event.pageY);
            } else if (icon) {
                icon.style.display = 'none'; // Hide the icon if no text is selected
            }
        });
    
    }

    // Function to show custom icon near the cursor
    function showCustomIcon(selection, mouseX, mouseY) {
        let icon = document.getElementById('custom-icon');
        if (!icon) {
            icon = document.createElement('div');
            icon.id = 'custom-icon';
            icon.style.position = 'absolute';
            icon.style.width = '30px';
            icon.style.height = '30px';
            icon.style.background = 'url(https://i.imgur.com/bgV3MEU.png) no-repeat center center';
            icon.style.backgroundSize = 'contain';
            icon.style.cursor = 'pointer';
            icon.style.zIndex = '9999'; // Ensure the icon is on top
            document.body.appendChild(icon);

            icon.addEventListener('mousedown', (e) => {
                e.preventDefault();
                setTimeout(() => {
                    const selectedText = selection.toString().trim();
                    processSelectedText(selectedText);
                }, 0);
            });
        }

        icon.style.display = 'block'; // Show the icon
        icon.style.left = `${mouseX + 5}px`;
        icon.style.top = `${mouseY + 5}px`;
    }
        // Function to process the selected text
    //選取內文判斷是否惡意
    async function processSelectedText(text) {
        console.log(`Processing selected text: ${text}`);
        let icon = document.getElementById('custom-icon');
        icon.style.display = 'none'; // hide the icon
        window.getSelection().removeAllRanges();
        navigator.clipboard.writeText(text);
        const newTab = window.open('http://127.0.0.1:8000', '_blank');

    };
    


    // Initial function to handle text selection
    TextSelectionHelper();
})();
