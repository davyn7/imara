# Imara's Internal Trading Tool

## Introduction

## Infrastructure

Backend: Python FastAPI  
Database: Supabase  
Deployment: Railway    
Frontend: Retool

## DB Schemas

##### Activity Log `{activity_log}`
##### Companies `{companies}`
##### Counterparties `{counterparties}`
##### Trades `{trades}`
##### Trade Costs `{trade_costs}`
##### Brokerage Deals `{brokerage_deals}`
##### Shipments `{shipments}`
##### Equity Rounds `{equity_rounds}`
##### Shareholders `{shareholders}`
##### Share Transactions `{share_transactions}`

## API Docs

### Basic CRUD Operations

The following are the basic CRUD operations that are available for each schema object:  
* Function: `get_{objects}`, Router [GET]: `/{objects}`
* Function: `get_{object}`, Router [GET]: `/{objects}/{object_id}`
* Function: `add_{object}`, Router [POST]: `/add_{object}`
* Function: `update_{object}`, Router [PUT]: `/update_{object}/{object_id}`
* Function: `delete_{object}`, Router [DELETE]: `/delete_{object}/{object_id}`
* Function: `delete_{objects}`, Router [DELETE]: `/delete_{objects}`

