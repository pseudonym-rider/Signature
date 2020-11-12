#include <groupsig/groupsig.h>
#include <stdio.h>
#include <stdbool.h>

#define B64_GPK_SIZE 2869

bool readGpk (groupsig_key_t *grpKey)
{
    char *szPath = "/home/suri/Desktop/COVID_Proto/groupsig/gpk";
    FILE *pFile = fopen(szPath, "r");

    if (pFile == NULL)
    {
        perror("fopen error");
        return false;
    }

    char base64Gpk[B64_GPK_SIZE]; // maybe 2868
    fgets(base64Gpk, B64_GPK_SIZE, pFile);
    fclose(pFile);

    message_t *tmp = message_from_base64(base64Gpk); // length maybe 2150

    groupsig_key_t *tmpGrpKey = groupsig_grp_key_init(GROUPSIG_BBS04_CODE);
    tmpGrpKey = groupsig_grp_key_import(GROUPSIG_BBS04_CODE, tmp->bytes, tmp->length);
    if (tmpGrpKey == NULL)
    {
        fprintf(stderr, "tmpGrpKey is NULL");
        return false;
    }

    groupsig_grp_key_copy(grpKey, tmpGrpKey);

    return true;
}

bool joinMember (groupsig_key_t *usrKey, groupsig_key_t *grpKey)
{
    char *szPath = "/home/suri/Desktop/COVID_Proto/groupsig/invitation";
    FILE *pFile = fopen(szPath, "r");

    if (pFile == NULL)
    {
        perror("fopen error");
        return false;
    }

    char base64Invitation[B64_GPK_SIZE];
    fgets(base64Invitation, B64_GPK_SIZE, pFile);
    fclose(pFile);

    message_t *msg1 = message_from_base64(base64Invitation);
    message_t *msg2 = message_init();
    groupsig_key_t *memberKey = groupsig_mem_key_init(GROUPSIG_BBS04_CODE);

    groupsig_join_mem(&msg2, memberKey, 1, msg1, grpKey);

    groupsig_mem_key_copy(usrKey, memberKey);

    return true;
}

bool signMessage (groupsig_key_t *memberKey, groupsig_key_t *grpKey)
{
    char *szPath = "/home/suri/Desktop/COVID_Proto/groupsig/MessageSignatureFromC";
    char *data = "Hello, World! Plz";

    groupsig_signature_t *signature;
    message_t *message;
    char *b64Signature;
    int rc;
    uint8_t b;

    signature = groupsig_signature_init(grpKey->scheme);

    message = message_from_string(data);
    if (message == NULL)
    {
        fprintf(stderr, "convert message error");
        return false;
    }

    rc = groupsig_sign(signature, message, memberKey, grpKey, UINT_MAX);
    if (rc != IOK)
    {
        fprintf(stderr, "sign error");
        return false;
    }

    rc = groupsig_verify(&b, signature, message, grpKey);
    if (rc != IOK || b != 1)
    {
        fprintf(stderr, "invalid signature");
        return false;
    }

    b64Signature = groupsig_signature_to_string(signature);

    FILE *pFile = fopen(szPath, "w");

    if (pFile == NULL)
    {
        perror("fopen error");
        return false;
    }

    fputs(data, pFile);
    fputs("\n", pFile);
    fputs(b64Signature, pFile);

    fclose(pFile);
    return true;
}


int main ()
{
    groupsig_config_t *cfg = groupsig_init(GROUPSIG_BBS04_CODE, 0);

    groupsig_key_t *grpKey = NULL;
    groupsig_key_t *usrKey = NULL;

    grpKey = groupsig_grp_key_init(GROUPSIG_BBS04_CODE);
    usrKey = groupsig_grp_key_init(GROUPSIG_BBS04_CODE);

    while (true)
    {
        int nMenu;

        printf("---------menu---------\n");
        printf("1. setup member (read group public key)\n");
        printf("2. join member list \n");
        printf("3. sign message\n");
        printf("4. exit\n");
        printf("input > ");
        scanf("%d", &nMenu);

        if (nMenu == 1)
        {
            if (! readGpk(grpKey))
            {
                fprintf(stderr, "readGpk() returns false");
                continue;
            }

            printf("\nwelcome!\n\n");

            /*
            byte_t *bytes;
            uint32_t size;
            bytes = NULL;

            int rc = groupsig_grp_key_export(&bytes, &size, grpKey);
            printf("%d\n", rc);
            message_t *tmpmessage = (message_t *)malloc(sizeof (message_t));
            tmpmessage->bytes = bytes;
            tmpmessage->length = size;
            char *b64key = message_to_base64(tmpmessage);
            printf("%s\n", b64key);
            printf("WOW\n");
            */
        }
        if (nMenu == 2)
        {
            if (! joinMember(usrKey, grpKey))
            {
                fprintf(stderr, "joinMember() returns false");
                continue;
            }

            printf("\njoin success!\n\n");
        }
        if (nMenu == 3)
        {
            if (! signMessage(usrKey, grpKey))
            {
                fprintf(stderr, "signMessage() returns false");
                continue;
            }

            printf("\ncreate message + signature message\n\n");
        }
        if (nMenu == 4) break;
    }

    return 0;
}
