#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 19:27:38 2020

@author: tfinney
"""

import subprocess
import urllib.request
import platform

def fetch_url_request(url,output_file):
    """
    The easist way to do it.
    """
    urlResponse = urllib.request.urlopen(url)
    
    urlOut = open(output_file,'wb')
    urlOut.write(urlResponse.read())
    urlOut.close()
    return True
    
    
def fetch_url_liar(url,output_file):
    """
    misrepresent yourself on the internet to confuse the sacbee
    """
    
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    hdr = {'User-Agent': user_agent}    
    req = urllib.request.Request(url, headers=hdr)
    
    url_response = urllib.request.urlopen(req)
    
    url_out = open(output_file,'wb')
    url_out.write(url_response.read())
    url_out.close()
    return True
    

def fetch_wget(url,output_file):
    """
    use our trusty friend "wget"
    """
    if platform.system() == 'Windows': #require WSL for windows
        cmd = ['wsl','wget','-O',str(output_file),str(url)]
    else:
    # advanced_cmd = ['wget','-O',str(output_file),'--tries=1','--timeout=30',str(url)]
        cmd = ['wget','-O',str(output_file),str(url)]
    subprocess.check_output(cmd)
    return True
    
def decompose_sacbee(url):
    """
    figured out the sacbee's obfuscation technique....
    """
# url = "https://www.sacbee.com/news/local/sacramento-tipping-point/article244279997.html#storylink=mainstage_card4"

    if url.find('www.sacbee.com') != -1:
        # print(True)
        
        start = url.find("article")
        end = url.find(".html")
        
        # print(start,end)
        # print(url[start:end])
        
        article_id = url[start:end] + '.html'
        article_url = 'https://www.sacbee.com/' + article_id
        # print(article_url)    
        return article_url
    
    else: #its not a sacbee piece
        return None
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    