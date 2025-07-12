from model import PortfolioRequest, PortfolioResponse
from generate_currency_code import settings
from agent import graph
from generate_image import generate_currency_image


from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse


app = FastAPI(title="Currency Conversion API", version="1.0")


@app.post("/convert", response_model=PortfolioResponse)
def convert_currency_endpoint(payload: PortfolioRequest):
    """Endpoint to convert currency based on user input."""
    
    if not payload.usd_amount or not payload.user_input:
        raise HTTPException(status_code=400, detail="USD amount and user input are required.")
    
    try:
        result = graph.invoke({
            "usd_amount": payload.usd_amount,
            "user_input": payload.user_input
        })
        image_base64 = generate_currency_image(result["target_currency"])

        return result
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/generate-image")
async def generate_image(currency: str):
    try:
        image_base64 = generate_currency_image(currency.upper())
        return JSONResponse(content={"image_base64": image_base64})
    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
