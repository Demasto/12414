import {API} from "../api";

const api = new API('goods')

export type Product = { "id": 3, "hs_code": "8472 90", "name": "Банкоматы" }

export interface ByYear {
    "year": 2022,
    "value_usd_mln": 286
}

export interface ImportsByYear extends ByYear {
    "country": "Taipei, Chinese",
    "value_tons": 0,
    "country_group": "friendly"
}

export type ProductInfo = {
    "good": {
        "id": 1,
        "hs_code": "8428 10",
        "name": "Лифты"
    },
    "tariffs": [
        {
            "applied_rate": number,
            "wto_bound_rate": number
        }
    ],
    "production": ByYear[],
    consumption: ByYear[],
    imports: ImportsByYear[],
    "flags": [{
        "in_techreg": true,
        "in_pp1875": true,
        "in_order4114": false
    }],
    "measures": [
        "Мера 6"
    ],
    "summary": {
        "last_year": 2024,
        "share_ns": 32.1746555252832,
        "delta_ns": -0.563999999999993,
        "prod_ge_cons": true,
        "applied": 0,
        "wto_bound": 0.05,
        "metric_used": "value_usd_mln",
        "branch": "вне текста"
    }
}

export class GoodsAPI {

    static getAll() {
        return api.get<Product[]>()
    }

    static get(id: string) {
        return api.get<ProductInfo>({
            methodName: 'dashboard',
            subId: id
        })
    }

    static chat(id: string, text: string) {
        return api.post<{ answer: string }>({question: text},{
            methodName: 'chat',
            subId: id,
        })
    }

    // static map(id:string) {
    //     return api.get({
    //         methodName: 'imports',
    //         subId: id,
    //         params: {
    //             year: '2024'
    //         }
    //     })
    // }


    //POST /api/chat — чат с ИИ (RAG по твоему локальному индексу)
    //
    // POST /api/mosprom-letter/{good_id} — вернёт DOCX-файл обращения (скачивание)
}