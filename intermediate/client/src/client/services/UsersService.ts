/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ResponseMessage } from '../models/ResponseMessage';
import type { User } from '../models/User';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class UsersService {

    /**
     * Create User
     * @param requestBody 
     * @returns ResponseMessage Successful Response
     * @throws ApiError
     */
    public static createUser(
requestBody: User,
): CancelablePromise<ResponseMessage> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/users/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
