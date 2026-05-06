# Imara's Internal Trading Tool

## Introduction

## Infrastructure

Backend: Python FastAPI  
Database: Supabase  
Deployment: Railway    
Frontend: Retool

## DB Schemas

##### Activity Log `{activity_log}`
* Any API calls and changes to DB will be logged into this schema.
##### Companies `{companies}`
* Imara-owned companies.
##### Counterparties `{counterparties}`
* Any entity that Imara is involved with.
##### Trades `{trades}`
* Imara's trading logs.
##### Trade Costs `{trade_costs}`
* Any costs associated to a particular trade.
##### Brokerage Deals `{brokerage_deals}`
* Imara's brokerage deal log.
##### Shipments `{shipments}`
* Shipments associated to a particular trade.
##### Equity Rounds `{equity_rounds}`
* Any fundraise done by Imara.
##### Shareholders `{shareholders}`
* List of shareholders in each Imara entity.
##### Share Transactions `{share_transactions}`
* Any form of share transactions.

## API Docs

### Basic CRUD Operations

The following are the basic CRUD operations that are available for each schema object:  
* Function: `get_{objects}()`, Router [GET]: `/{objects}`
* Function: `get_{object}()`, Router [GET]: `/{objects}/{object_id}`
* Function: `add_{object}()`, Router [POST]: `/add_{object}`
* Function: `update_{object}()`, Router [PUT]: `/update_{object}/{object_id}`
* Function: `delete_{object}()`, Router [DELETE]: `/delete_{object}/{object_id}`
* Function: `delete_{objects}()`, Router [DELETE]: `/delete_{objects}`

### Advanced API Operations

Some 

#### Calculating trade costs and distribution

#### Creating a new trade
* Function: `add_trade_ext()`, Router [POST]: `/add_trade_ext`
* To create a new trade, there must be a seller and buyer that has been inputted into the 

#### Creating a new shareholder
* Function: `add_shareholder_ext()`, Router [POST]: `/add_shareholder_ext`
* Parameters:
    * `shareholder: ShareholderBase`
    * `add_type: str`, either _basic_ or _fundraise_
* Check if `shareholder` is in `Counterparties`
* If `add_type` is _basic_
Must check if shareholder is in counterparty -> Maybe check by name?  
If yes, then add shareholder as per normal  
If not, then add counterparty, label as investor, and then add shareholder to DB

#### Creating a new equity round
* Function: `add_round_ext()`, Router [POST]: `/add_round_ext`
* Call the `/add_equity_round` API.
* For each of the investors participating in the round, check:
    * If shareholder is in `counterparties` and in `shareholders` for that `company_id`, call the `/update_shareholder/{shareholder_id}` API.
    * If shareholder is in `counterparties` but not in `shareholders` for that `company_id`, call the `/add_shareholder` API.
    * If shareholder is not in `counterparties` yet, call `/add_counterparty` API to register the new shareholder as a counterparty.
* Calculate the number of shares allocated per investor.
* Call the `add_share_transaction` API to create a share transaction per investor.
