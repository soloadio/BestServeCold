import { Injectable } from '@angular/core';
import { GoogleGenAI } from "@google/genai";
import { environment } from '../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class Geminiservice {

  ai = new GoogleGenAI({apiKey: environment.GEMINI_API_KEY});

  private getHeader(content: string) {
    return {
      model: "gemini-2.5-flash",
      contents: content,
    }
  }

  generateResponse(content: string){
    this.ai.models.generateContent(this.getHeader(content))
  }
}
