import { User } from './user';
import { Category } from './category';
export interface Job {
    category: Category,
    employee?: User,
    hasAccepted: boolean,
    timestamp: string
}
